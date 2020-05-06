__copyright__ = "Reiner Lemoine Institut"
__license__   = "GNU Affero General Public License Version 3 (AGPL-3.0)"
__url__       = "https://github.com/openego/data_processing/blob/master/LICENSE"
__author__    = "Ludee, jh-RLI"

import os
from collections import namedtuple
from typing import List
import json
import logging
import pandas as pd
import pathlib
import jmespath
import getpass
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
import oedialect
import geopandas as gpd
from geoalchemy2.types import Geometry

from postgresql_types import TYPES


# prepare connection string to connect via oep API
CONNECTION_STRING = "{engine}://{user}:{token}@{host}"
#
DB = namedtuple("Database", ["engine", "metadata"])


class CredentialError(Exception):
    pass


class DatabaseError(Exception):
    pass


class MetadataError(Exception):
    pass


def setup_db_connection(engine="postgresql+oedialect", host="openenergy-platform.org"):
    try:
        user = os.environ["OEP_USER"]
    except KeyError:
        user = input("Enter OEP-username:")
    try:
        token = os.environ["OEP_TOKEN"]
    except KeyError:
        token = getpass.getpass("OEP-Token:")

    # Generate connection string:
    conn_str = CONNECTION_STRING
    conn_str = conn_str.format(
        engine=engine, user=user, token=token, host=host
    )

    engine = sa.create_engine(conn_str)
    metadata = sa.MetaData(bind=engine)
    return DB(engine, metadata)


def create_tables(db: DB, tables: List[sa.Table]):
    for table in tables:
        if not db.engine.dialect.has_schema(db.engine, table.schema):
            logging.info(f'The provided database schema: "{table.schema}" does not exist. Please use an existing schema')
        else:
            if not db.engine.dialect.has_table(db.engine, table.name, table.schema):
                try:
                    print(table)
                    table.create()
                    logging.info(f"Created table {table.name}")
                except sa.exc.ProgrammingError:
                    logging.error(f'Table "{table.name}" already exists')
                    raise


def order_tables_by_foreign_keys(tables: List[sa.Table]):
    """
    This function tries to order tables to avoid missing foreign key errors.

    By now, ordering is simply done by counting of foreign keys.
    """
    return sorted(tables, key=lambda x: len(x.foreign_keys))


def create_tables_from_metadata_file(db: DB, metadata_file: str) -> List[sa.Table]:
    with open(metadata_file, "r") as metadata_json:
        metadata = json.loads(metadata_json.read())
    tables_raw = jmespath.search("resources", metadata)

    tables = []
    for table in tables_raw:
        # Get (schema) and table name:
        schema_table_str = table["name"].split(".")
        if len(schema_table_str) == 1:
            schema = "model_draft"
            table_name = schema_table_str[0]
        elif len(schema_table_str) == 2:
            schema, table_name = schema_table_str
        else:
            raise MetadataError("Cannot read table name (and schema)", table["name"])

        # Get primary keys:
        primary_keys = jmespath.search("schema.primaryKey[*]", table)

        # Get foreign_keys:
        foreign_keys = {
            fk["fields"][0]: fk["reference"]
            for fk in jmespath.search("schema.foreignKeys", table)
        }

        # Create columns:
        columns = []
        for field in jmespath.search("schema.fields[*]", table):
            # Get column type:
            try:
                column_type = TYPES[field["type"]]
            except KeyError:
                raise MetadataError(
                    "Unknown column type", field, field["type"], metadata_file
                )

            if field["name"] in foreign_keys:
                foreign_key = foreign_keys[field["name"]]
                column = sa.Column(
                    field["name"],
                    column_type,
                    sa.ForeignKey(
                        f'{foreign_key["resource"]}.{foreign_key["fields"][0]}'
                    ),
                    primary_key=field["name"] in primary_keys,
                    comment=field["description"],
                )
            else:
                column = sa.Column(
                    field["name"],
                    column_type,
                    primary_key=field["name"] in primary_keys,
                    comment=field["description"],
                )
            columns.append(column)

        tables.append(sa.Table(table_name, db.metadata, *columns, schema=schema))
    return tables


if __name__ == "__main__":
    logger = logging.getLogger()

    metadata_folder = input("Enter metadata folder name:")
    folder = pathlib.Path.cwd() / metadata_folder
    print(folder)
    metadata_files = [str(file) for file in folder.iterdir()]

    db = setup_db_connection()

    tables = []
    for metadata_file in metadata_files:
        try:
            md_tables = create_tables_from_metadata_file(db, metadata_file)
            print(md_tables)
        except:
            logger.error(
                f'Could not generate tables from metadatafile "{metadata_file}"'
            )
            raise
        tables.extend(md_tables)
    ordered_tables = order_tables_by_foreign_keys(tables)
    create_tables(db, ordered_tables)

    # gdf_awz = gpd.read_file("bsh_seegrenzen_awz.gpkg")
    # print(gdf_awz)

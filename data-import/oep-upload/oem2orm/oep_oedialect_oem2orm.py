__copyright__ = "Reiner Lemoine Institut"
__license__   = "GNU Affero General Public License Version 3 (AGPL-3.0)"
__url__       = "https://github.com/openego/data_processing/blob/master/LICENSE"
__author__    = "henhuy, jh-RLI"

import os
from collections import namedtuple
from typing import List
import json
import logging
import pathlib
import jmespath
import getpass
import sqlalchemy as sa
import re
from sqlalchemy.orm import sessionmaker
import oedialect

from .postgresql_types import TYPES


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


def setup_logger():
    """
    Easy logging setup depending on user input. Provides a logger for INFO level logging.
    :return: logging.INFO or none
    """
    logger_level = input("Display logging information[Yes] or [No]:")
    if re.fullmatch('[Yy]es', logger_level):
        print('logging activated')
        return logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    elif re.fullmatch('[Nn]o', logger_level):
        pass


def setup_db_connection(engine="postgresql+oedialect", host="openenergy-platform.org"):
    """
    Create SQLAlchemy connection to Database API with Username and Token.
    Default is the OEP RESTful-API.

    :param engine: Database engine, default is postgresql
    :param host: API provider
    :return: DB(sa.engine, sa.metadata) namedtuple
    """

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
    """
    Creates a SQLAlchemy create ORM table-objects via API connection on a Database.
    The tables can be a list of ORM.

    :param db: API
    :param tables: SQLAlchemy ORM objects (automatically retrieved from OEM json strings)
    :return: none
    """
    for table in tables:
        if not db.engine.dialect.has_schema(db.engine, table.schema):
            logging.info(f'The provided database schema: "{table.schema}" does not exist. Please use an existing schema')
        else:
            if not db.engine.dialect.has_table(db.engine, table.name, table.schema):
                try:
                    print(table)
                    table.create(checkfirst=True)
                    logging.info(f"Created table {table.name}")
                except sa.exc.ProgrammingError:
                    logging.error(f'Table "{table.name}" already exists')
                    raise


def delete_tables(db: DB, tables: List[sa.Table]):
    """
    Drop all tables stored in the sqlalchemy metadata object. The tables are sorted by
    foreign key and dropped one by one. Each drop interaction requires the user to
    confirm the action.

    :param db: sqla engine and metadata object
    :param tables:
    :return: none
    """

    ordered_tables = order_tables_by_foreign_keys(tables)
    reversed_tables = reversed(ordered_tables)

    print("Please confirm that you would like to drop the following tables:")
    for n, tab in enumerate(tables):
        print("{: 3d}. {}".format(n, tab))

        print("Please confirm with either of the choices below:\n" +
              "- yes\n" +
              "- no\n" +
              "- the indexes to drop in the format 0, 2, 3, 5")
        confirmation = input(
            "Please type the choice completely as there is no default choice.")
        if re.fullmatch('[Yy]es', confirmation):
            for tab in reversed_tables:
                tab.drop(db.engine, checkfirst=True)
        elif re.fullmatch('[Nn]o', confirmation):
            print("Cancelled dropping of tables")


def order_tables_by_foreign_keys(tables: List[sa.Table]):
    """
    This function tries to order tables to avoid missing foreign key errors.

    By now, ordering is simply done by counting of foreign keys.
    """
    return sorted(tables, key=lambda x: len(x.foreign_keys))


def create_tables_from_metadata_file(db: DB, metadata_file: str) -> List[sa.Table]:
    """
    Takes a metadata file in oem format (tested with oem v1.4.0) and
    generates a sqlalchemy ORM Table representation. The oem can contain
    multiple Tables, this function will return one or multiple sa table objects.

    :param db: API
    :param metadata_file: json file (oem 1.4.0)
    :return: collection of sqlalchemy table objects
    """
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

        if check_oep_api_schema_whitelist(schema):
            tables.append(sa.Table(table_name, db.metadata, *columns, schema=schema, extend_existing=True))
        else:
            logging.info("The current schema:'" + schema + "' is changed to 'model_draft'")
            schema = "model_draft"
            tables.append(sa.Table(table_name, db.metadata, *columns, schema=schema, extend_existing=True))
    return tables


def check_oep_api_schema_whitelist(oem_schema):
    """
    Check if the used schema is supported by the oep-api. Implementing api restrictions.

    :param oem_schema:string
    :return: bool
    """
    api_open_schema = ['model_draft', 'sandbox']

    if oem_schema in api_open_schema:
        return True
    else:
        logging.info("The OEP-API does not allow to write un-reviewed data to another schema then model_draft or sandbox")
        return False


def select_oem_dir(oem_folder_name=None, filename=None):
    """
    Select the metadata directory or file that is used to generate the tables.
    The default is the current directory (where you execute the script from)
    inside a folder called oem_folder.

    :param oem_folder_name:
    :param filename:
    :return: string (path to current directory + folder name) or none
    """
    if oem_folder_name is not None:
        oem_path = pathlib.Path.cwd() / oem_folder_name
        return oem_path
    elif oem_folder_name is 'default':
        pass
        # default_oem_path =
    else:
        raise FileNotFoundError


def collect_ordered_tables_from_oem(db: DB, oem_folder_path):
    tables = []
    metadata_files = [str(file) for file in oem_folder_path.iterdir()]

    for metadata_file in metadata_files:
        try:
            md_tables = create_tables_from_metadata_file(db, metadata_file)
            logging.info(md_tables)
        except:
            logging.error(
                f'Could not generate tables from metadatafile: "{metadata_file}"'
            )
            raise
        tables.extend(md_tables)

    fk_ordered_tables = order_tables_by_foreign_keys(tables)

    return fk_ordered_tables


if __name__ == "__main__":
    # Easy cmd usage and testing (development purpose)

    logger = logging.getLogger()

    metadata_folder = input("Enter metadata folder name:")
    # ToDo: add the review-oemetadata path
    folder = pathlib.Path.cwd() / metadata_folder
    metadata_files = [str(file) for file in folder.iterdir()]

    db = setup_db_connection()

    tables = []
    for metadata_file in metadata_files:
        try:
            md_tables = create_tables_from_metadata_file(db, metadata_file)
            logger.info(md_tables)
        except:
            logger.error(
                f'Could not generate tables from metadatafile: "{metadata_file}"'
            )
            raise
        tables.extend(md_tables)
    ordered_tables = order_tables_by_foreign_keys(tables)
    create_tables(db, ordered_tables)

    delete_tables(db, tables)

    # gdf_awz = gpd.read_file("bsh_seegrenzen_awz.gpkg")
    # print(gdf_awz)
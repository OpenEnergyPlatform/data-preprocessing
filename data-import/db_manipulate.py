# -*- coding: utf-8 -*-

"""
Service functions for oedb

This file is part of project OEDB (https://github.com/).
It's copyrighted by the contributors recorded in the version control history:


SPDX-License-Identifier: AGPL-3.0-or-later
"""

__copyright__ = "© Reiner Lemoine Institut"
__license__ = "GNU Affero General Public License Version 3 (AGPL-3.0)"
__license_url__ = "https://www.gnu.org/licenses/agpl-3.0.en.html"
__author__ = "jh-RLI"
__version__ = "v0.0.1"


import os
import re
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry
import shapefile
from .db_io import db_session
from .db_logger import LogClass
import sqlalchemy
from sqlalchemy import Table, Column, Integer
# from db_store import


# db connecion
con = db_session()
insp = sqlalchemy.inspect(con)
metadata = sqlalchemy.MetaData()
log = LogClass()
Base = declarative_base()


DEFAULT_SCHEMA = 'orig_vg250'
DEFAULT_TABLE = 'importtest'


# set download folder
download_folder = r'C:\eGoPP\vg250'
testpfad = (
    r'C:\eGoPP\vg250\vg250_2016-01-01.gk3.shape.ebenen\
    vg250_2016-01-01.gk3.shape.ebenen\vg250_ebenen\VG250_GEM'
)


# ORM
'''
class Table(Base):
    # set Table
    __tablename__ = DEFAULT_TABLE
    id      = Column(Integer, primary_key=True, nullable=false)
    geom    = Column(Geometry)
    schema  = 'orig_vg250'
'''

# create session
Session = sessionmaker()
Session.configure(bind=con)
session = Session()


class BaseDataLoader:
    """

            Parameters
            -------
    """

    shapefilename = ""
    columns = set()

    @staticmethod
    def load_file():
        """
        Get all .shp files out of a download, creats a list of the path of the
        shapefiles
        Optional: Make downloadfolder dynamic

        Parameters
        --------


        """

        full_dir = os.walk(download_folder)
        shapefile_list = []
        path_save = []
        for dirpaths, _, files in full_dir:
            for file_ in files:
                if file_[-3:] == 'shp':

                    # path
                    shapefile_path = os.path.join(dirpaths, file_)
                    # log.logger().info("Shapefile path: " + shapefile_path)

                    # extract date from string
                    parent_folder = os.path.basename(os.path.abspath(
                        os.path.join(dirpaths, os.pardir)))
                    regex_pattern = re.compile('_[0-9-]*.gk3')
                    match = regex_pattern.search(parent_folder)[0]
                    date_str = match[1:-4]

                    # table
                    table_name = (
                            os.path.join(file_)[:-4] + "_" +
                            date_str
                    )
                    # log.logger().info("Table name: " + table_name)
                    path_save.append(shapefile_path)
                    entry = [shapefile_path, table_name]
                    shapefile_list.append(entry)

                    """ Testing
                    # print("Shapelist:" + str(shapefile_list))
                    # print("Path:" + str(shapefile_path))

                    #read the shapefile
                    #shape = shapefile.Reader(shapefile_path)
                    # all records (attributes in dbf record) in shapefile
                    #shape_records = shape.shapeRecords()



                    #Hand to next Method
                    #self.process_shapes(shape_records)


                    
                    # first feature of the shapefile
                    feature = shape.shapeRecords()
                    first = feature.shape.__geo_interface__

                    # print(shape_save)
                    # print(first)

                    from shapely.geometry import shape
                    shp_geom = shape(first)
                    # print(shp_geom)
                    shape_save.append(shp_geom.wkb)
                    # print(shp_geom)
                    print(type(shp_geom))
                    """

        # log.logger().info("Shapefile list: '{}'".format(shapefile_list))
        # print(sys.getsizeof(shape_save))
        # print("Start: " + str(shape_save))
        # print("Loaded shapefile features: " + str(len(shape_save)))
        return path_save

        # Method call
        # self.get_shp_values(path_save)

    def get_shp_values(self, path_save):
        """
        Loads shapefile to python
        Get the values out of every ESRI .shp file (file path: path_save)
        Reads the geometry and the attributes out of the Shapefile using
        PyShape
        -------
        :param path_save:
        """

        # loops trough all shapefile in path_save and saves the column names to
        # list
        for path in path_save:
            pathname = path[:-4]
            # get record field names to create table
            with open(pathname + '.shp', 'rb') as shp_file:
                with open(pathname + '.dbf', 'rb') as dbf_file:
                    shape = shapefile.Reader(shp=shp_file, dbf=dbf_file)
            fields = shape.fields[1:]
            field_names = {field[0] for field in fields}
            self.columns.update(field_names)

        # Method call with all column names in the current shapefile
        self.mktbl()

    def mktbl(self):
        """
            Creates Table with all necessary attributes to insert the
            data from shapefile
        """

        # set Table (not ORM)
        test_import_tbl1 = Table(
            DEFAULT_TABLE,
            metadata,
            Column('id', Integer, primary_key=True, nullable=False),
            Column('geom', Geometry),
            schema=DEFAULT_SCHEMA
        )

        # check if table exist, create base table | mind static schema and
        # table name
        if DEFAULT_TABLE not in insp.get_table_names(DEFAULT_SCHEMA):
            # test_import_tbl1.drop(con)
            test_import_tbl1.create(con)

            # ORM
            # Base.metadata.create_all(bind=con)

        # test ORM insert
        # TODO: Change Tabele to ORM

        # Get all column names in the DB Table by key out of an dict
        c_temp = [
            c['name']
            for c in insp.get_columns(DEFAULT_TABLE, DEFAULT_SCHEMA)
        ]

        # update/add the columns form shapefile to the table if they not exist
        # Note: not able to distinguish between column names which name is the
        # same but one or all letters are in written in cpas
        # (Example | example = the same)
        for column in self.columns:
            if column.lower() not in c_temp:
                # for typ in typ_temp:
                con.execute(
                    f'ALTER TABLE {DEFAULT_SCHEMA}.{DEFAULT_TABLE} '
                    f'ADD COLUMN {column} varchar'
                )
            else:
                print("Column " + column + " already exists!")

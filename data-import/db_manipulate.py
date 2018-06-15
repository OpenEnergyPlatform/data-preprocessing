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
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import *
import shapefile
import dateutil.parser as dparser
from db_io import db_session
from db_logger import LogClass
from sqlalchemy import *
#from db_store import



#db connecion
con = db_session()
insp = inspect(con)
metadata = MetaData()
log = LogClass()
Base = declarative_base()


# set download folder
download_folder = r'C:\eGoPP\vg250'
testpfad = r'C:\eGoPP\vg250\vg250_2016-01-01.gk3.shape.ebenen\vg250_2016-01-01.gk3.shape.ebenen\vg250_ebenen\VG250_GEM'


#ORM
'''
class Table(Base):
    # set Table
    __tablename__ = 'importtest'
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
    tbl_list = []
    ac = []




    def load_file(self):
        """
        Get all .shp files out of a download, creats a list of the path of the shapefiles
        Optional: Make downloadfolder dynamic

        Parameters
        --------


        """

        full_dir = os.walk(download_folder)
        shapefile_list = []
        path_save = []
        for dirpaths, dirnames, files in full_dir:
            for file_ in files:
                if file_[-3:] == 'shp':

                    # path
                    shapefile_path = os.path.join(dirpaths, file_)
                    # log.logger().info("Shapefile path: " + shapefile_path)

                    # extract date from string
                    s = dirpaths.replace('\\', " ").replace('\v', ' ')
                    # print(s)
                    remove1 = [':', '/', '\\', '_', '.']
                    for char in remove1:
                        s = s.replace(char, " ")
                    remove2 = ['C', 'vg250', 'g250', 'ebenen', 'gk3', 'eGoPP', 'shape', 'historisch', 'de0001',
                               'de0101', 'de0201', 'de0301', 'de0401', 'de0501', 'de0601', 'de0701', 'de0801', 'de0901',
                               'de1001', 'de1101', ' ', 'mv', 'kreisreform', ' ']
                    for char in remove2:
                        s = s.replace(char, "")
                    clean_str = s[:-10]
                    # print(clean_str)
                    date_str = dparser.parse(clean_str, fuzzy=True).date()
                    # table
                    table_name = os.path.join(file_)[:-4] + "_" + date_str.strftime('%Y-%m-%d')
                    # log.logger().info("Table name: " + table_name)
                    path_save.append(shapefile_path)
                    entry = []
                    entry.append(shapefile_path)
                    entry.append(table_name)
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


        #log.logger().info("Shapefile list: '{}'".format(shapefile_list))
        #print(sys.getsizeof(shape_save))
        #print("Start: " + str(shape_save))
        #print("Loaded shapefile features: " + str(len(shape_save)))
        return path_save

        #Method call
        #self.get_shp_values(path_save)






    def get_shp_values (self, path_save):
        """
        Loads shapefile to python
        Get the values out of every ESRI .shp file (file path: path_save)
        Reads the geometry and the attributes out of the Shapefile using PyShape
        -------
        :param path_save:
        """

        #loops trough all shapefile in path_save and saves the column names to list
        for path in path_save:
            # get record field names to create table
            shape = shapefile.Reader(path)
            fields = shape.fields[1:]
            field_names = [field[0] for field in fields]
            self.ac.extend(field_names)


        # Method call with all column names in the current shapefile
        self.mktbl(self.ac)



    def mktbl(self, ac):
        """
            Creates Tabel with all necessary attributes to insert the
            data from shapefile

        ----------
        :param ac:
        """



        #find all duplicates in list and saves "clean" list to list
        for j in ac:
            if j not in self.tbl_list:
                self.tbl_list.append(j)


        print(self.tbl_list)
        print(len(self.tbl_list))


        # set Table (not ORM)
        test_import_tbl1 = Table('importtest', metadata,
                                 Column('id', Integer, primary_key=True, nullable=false),
                                 Column('geom', Geometry),
                                 schema='orig_vg250')


        # check if table exist, create base table | mind static schema and table name
        if 'importtest' not in insp.get_table_names('orig_vg250'):
            #test_import_tbl1.drop(con)
            test_import_tbl1.create(con)

            #ORM
            #Base.metadata.create_all(bind=con)


        #test ORM insert
        #ToDO: Change Tabele to ORM



        # Get all column names in the DB Table by key out of an dict
        c_temp = []
        typ_temp = []
        for c in insp.get_columns('importtest','orig_vg250'):
            c_temp.append(c['name'])


        # update/add the columns form shapefile to the table if they not exist
        # Note: not able to distinguish between column names which name is the same but one or all letters are in written in cpas (Example | example = the same)
        for j in self.tbl_list:
            if j.lower() not in c_temp:
                #for typ in typ_temp:
                con.execute('ALTER TABLE {} ADD COLUMN {} varchar'.format('orig_vg250.importtest', j))
            else:
                print("Column " + j + " already exists!")




#ToDO: Delete all lines that exist only for testing purpose
#l = BaseDataLoader()
#l.get_shp_values(l.load_file())




#con.close()
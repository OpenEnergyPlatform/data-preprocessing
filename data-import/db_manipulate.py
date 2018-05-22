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
__author__ = "Jonas Huber"
__version__ = "v0.1.3"


from sqlalchemy import *
from shapely.wkb import loads, dumps
#from osgeo import ogr
import shapefile
import os, subprocess
import dateutil.parser as dparser
from db_io import *
from db_logger import *



con = db_session()

""" Daten aus der Datenbank

class Geometry(types.TypeEngine):

    def __init__(self, srid, geom_type, dims=2):
        super(Geometry, self).__init__()
        self.srid = srid
        self.geom_type = geom_type
        self.dims = dims

    def get_col_spec(self):
        return 'GEOMETRY()'

    def convert_bind_param(self, value, engine):
        if value is None:
            return None
        else:
            return "SRID=%s;%s" \
            % (self.srid, value.wkb.encode('hex'))

    def convert_result_value(self, value, engine):
        if value is None:
            return None
        else:
            return loads(value.decode('hex'))


metadata = MetaData(con)
places = Table("berlin", metadata, Column("einwohner"))

result = places.select().execute()

row = result.fetchone()

print(row)
print(row.keys())
"""

log = LogClass()

# create download folder
download_folder = r'C:\eGoPP\vg250'
testpfad = r'C:\eGoPP\vg250\vg250_2016-01-01.gk3.shape.ebenen\vg250_2016-01-01.gk3.shape.ebenen\vg250_ebenen\VG250_GEM'



#class DataLoader:
"""

        Parameters
        -------
"""



def load_file():
    """ Data

        Parameters
        --------

    """

    full_dir = os.walk(download_folder)
    shapefile_list = []
    shape_save = []
    for dirpaths, dirnames, files in full_dir:
        for file_ in files:
            if file_[-3:] == 'shp':
                # path
                shapefile_path = os.path.join(dirpaths, file_)
                #log.logger().info("Shapefile path: " + shapefile_path)

                # extract date from string
                s = dirpaths.replace('\\', " ").replace('\v', ' ')
                #print(s)
                remove1 = [':', '/', '\\', '_', '.']
                for char in remove1:
                    s = s.replace(char, " ")
                remove2 = ['C', 'vg250', 'g250', 'ebenen', 'gk3', 'eGoPP', 'shape', 'historisch', 'de0001',
                            'de0101', 'de0201', 'de0301', 'de0401', 'de0501', 'de0601', 'de0701', 'de0801', 'de0901',
                            'de1001', 'de1101', ' ', 'mv', 'kreisreform', ' ']
                for char in remove2:
                    s = s.replace(char, "")
                clean_str = s[:-10]
                #print(clean_str)
                date_str = dparser.parse(clean_str, fuzzy=True).date()

                # table
                table_name = os.path.join(file_)[:-4] + "_" + date_str.strftime('%Y-%m-%d')
                #log.logger().info("Table name: " + table_name)
                entry = []
                entry.append(shapefile_path)
                entry.append(table_name)
                shapefile_list.append(entry)
                #print("Shapelist:" + str(shapefile_list))
                #print("Path:" + str(shapefile_path))

                shape = shapefile.Reader(shapefile_path)
                # first feature of the shapefile
                feature = shape.shapeRecords()[0]
                first = feature.shape.__geo_interface__
                shape_save.append(first)
                #print(shape_save)
                #print(first)

    #log.logger().info("Shapefile list: '{}'".format(shapefile_list))
    print(shape_save)
    print("Loaded shapefile features: " + str(len(shape_save)))

    #thisfile = download_folder + "VG250_GEM"
    #print(thisfile)


    # def prase_to_sql (self):

    # def import_to_pgsqldb (self):



load_file()


con.close()





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
__version__ = "v0.1.3"


from sqlalchemy import *
from geoalchemy2 import *
import shapefile
import dateutil.parser as dparser
from db_io import *
from db_logger import *
from sqlalchemy import *



#db connecion
con = db_session()
metadata = MetaData()

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

# set download folder
download_folder = r'C:\eGoPP\vg250'
testpfad = r'C:\eGoPP\vg250\vg250_2016-01-01.gk3.shape.ebenen\vg250_2016-01-01.gk3.shape.ebenen\vg250_ebenen\VG250_GEM'



class DataLoader:
    """

            Parameters
            -------
    """
    temp = []
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

        #Method call
        self.get_shp_values(path_save)






    def get_shp_values (self, path_save):
        """
        Loads shapefile to python
        Get the values out of every ESRI .shp file (file path: path_save)
        Reads the geometry and the attributes out of the Shapefile using PyShape

        Parameters
        --------
        """
        #loops trough all shapefile in path_save and saves the column names to list
        for path in path_save:
            # get record field names to create table
            shape = shapefile.Reader(path)
            fields = shape.fields[1:]
            field_names = [field[0] for field in fields]
            print(len(field_names))
            self.ac.extend(field_names)


        # Method call with all column names in the current shapefile
        self.mktbl(self.ac)



    #example code
    # loop through each record in shapefile
    def process_shapes(self, shape_records):
        for record in shape_records:
            self.insert_shape(record)


    #example code
    # create the shape in the database
    def insert_shape(self, new_record):
        """ code from exampel
        tract_latln = new_record.record[10:]
        tract_number = new_record.record[2]
        con.execute("INSERT INTO importtest(lat, lng, tract_number) VALUES(%s, %s, %s) RETURNING id",
                    (float(tract_latln[1]), float(tract_latln[2]), tract_number))
        self.insert_points(new_record, con.fetchone()[0])
        """

    #example code
    # insert corrisponding boundary points for a given shape relation
    def insert_points(self, new_record, id):
        for point in new_record.shape.points:
            con.execute("INSERT INTO importtest_p(lat, lng, tract_id) VALUES(%s, %s, %s)",
                        (float(point[1]), float(point[2]), id))




    def mktbl(self, ac):
        """
                Creates Tabel with all necessary attributes to insert the
                data from shapefile

                Parameters
                --------


        """
        #find all duplicates in list and saves "clean" list to list
        for j in ac:
            if j not in self.tbl_list:
                self.tbl_list.append(j)


        print(self.tbl_list)
        print(len(self.tbl_list))


        """
        #create Table
        test_import_tbl1 = Table('importtest', metadata,
                                 Column('id', Integer, primary_key=True),
                                 Column('geom', Geometry('POLYGON')),
                                 schema='orig_vg250')

        test_import_tbl1.drop(con)
        test_import_tbl1.create(con)
        """

    def field_matches(self, ac):
        """
        compares existing list with the new list to get new field(table columns)


        -------
        """











l = DataLoader()
#l.mktbl()
l.load_file()







con.close()





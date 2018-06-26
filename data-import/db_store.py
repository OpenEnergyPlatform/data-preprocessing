# -*- coding: utf-8 -*-

"""
Service functions for oedb

This file is part of project OEDB (https://github.com/OpenEnergyPlatform).
It's copyrighted by the contributors recorded in the version control history:
#!!

SPDX-License-Identifier: AGPL-3.0-or-later
"""

__copyright__ = "© Reiner Lemoine Institut"
__license__ = "GNU Affero General Public License Version 3 (AGPL-3.0)"
__license_url__ = "https://www.gnu.org/licenses/agpl-3.0.en.html"
__author__ = "jh-RLI"
__version__ = "v0.0.1"


from db_manipulate import BaseDataLoader
from sqlalchemy import inspect, select
from shapely.geometry import shape
from geoalchemy2.shape import from_shape
from geoalchemy2.elements import WKBElement
import shapefile
from db_io import db_session

#ToDo: Implement logging
#from db_logger import *

l = BaseDataLoader()
con = db_session()
insp = inspect(con)


class StoreData:

    # set schema.table
    table_name = 'orig_vg250.importtest'

    def process_shp_files(self):
        """


        Parameters
        ----------

        :return:
        """
        # loops trough all shapefiles in path_save (load_file), gets all records
        for path in l.load_file():
            # get records to insert from shapefile
            sr = shapefile.Reader(path)
            shp_records = sr.shapeRecords()
            first_shp_records = sr.shapeRecords()[0]
            #Geometry ...
            shapes = sr.shapes()
            #Record values
            fields = sr.fields[1:]
            #lower() because column names in DB are also lowercase
            field_names = [field[0].lower() for field in fields]

            '''
            geoshp = first_shp_records.shape.__geo_interface__
            print(geoshp)
            '''

            for r in shp_records:
                geoshp = r.shape.__geo_interface__
                self.insert_shp_records(r, field_names, geoshp)



            '''
            for feature in shapes:
                geoshp = feature.sr.__geo_interface__
                self.insert_shp_geom(geoshp)
            '''




    def insert_shp_records(self, r, field_names, geoshp):
        """
        Parameters
        ----------
        :param r:
        :param field_names:
        :return:
        """
        v = r.record[0:]
        inputrecords = dict(zip(field_names, v))

        #ToDO: Implement Test (maybe use this?)
        # Get all column names in the DB Table by key out of an dict
        c_temp = []
        for c in insp.get_columns('importtest', 'orig_vg250'):
            c_temp.append(c["name"])

        geo = shape(geoshp)
        wkb_geo = from_shape(geo)
        # geomtype = type(geo)

        inputrecords['geom'] = geo.wkb_hex

        keys = inputrecords.keys()
        #collect all field names (column names) formats them for the query
        columns = ','.join(keys)
        #collect all values for key,vlaue pair in dict
        values = ','.join(['%({})s'.format(k) for k in keys])

        insert_rec = "INSERT INTO {} ({}) VALUES ({})".format(self.table_name, columns, values)

        con.execute(insert_rec, inputrecords)
        #self.insert_shp_geom(geoshp, curs.fetchone()[0])


    def insert_shp_geom(self, geoshp, id):
        """

        :param geoshp:
        :param insert_rec:
        :return:
        """
        geo = shape(geoshp)
        # geomtype = type(geo)

        column = 'geom'

        # ToDo: optional - Insert/Update with WKB Element
        # wkbgeo = from_shape(geo)
        # insert = "INSERT INTO {} ({}) VALUES (ST_GeomFromWKB(('{}'), 4326))".format(self.table_name, column, wkbgeo)
        # insert_geo = "INSERT INTO {} ({}) VALUES (ST_GeomFromText(('{}')))".format(self.table_name, column, geo)
        # ToDO:Update is not working in the way I need it
        update_geo = "UPDATE {} SET {}=ST_GeomFromText('{}') WHERE (id={}) ".format(self.table_name, column, geo, id)
        # UPDATE films SET kind = 'Dramatic' WHERE kind = 'Drama';

        # geomdict = {'geometry': wkbgeo}
        con.execute(update_geo)



    #ToDO: needs to be implemented / waiting for answer (pyshp github Issue #143)
    def record_type_todb (self, inputdict):
        """
        Parameters
        ----------
        :param inputdict:
        :return:
        """
        pass


#creats table
l.get_shp_values(l.load_file())
s = StoreData()
s.process_shp_files()


con.close()
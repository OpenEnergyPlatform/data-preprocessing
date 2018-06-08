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


import os, subprocess
import time
import urllib.request
import sqlalchemy
import shutil
import zipfile
import dateutil.parser as dparser

#mind file name changes
from db_io import *
from db_logger import *
from db_manipulate import *

# start time
total_time = time.time()

# delete eGoPP folder
eGoPP_folder = r'C:/eGoPP/'
# if os.path.exists(eGoPP_folder):
#     shutil.rmtree(eGoPP_folder)
#     time.sleep(3)

# create new eGoPP folder
if not os.path.exists(eGoPP_folder):
    os.makedirs(eGoPP_folder)

""" moved to db_log.py
# configure log
log = log.getlog('eGoPP')
log.setLevel(log.INFO)
# file handler (fh)
fh = log.FileHandler(r'C:/eGoPP/ego_pp.log')
fh.setLevel(log.INFO)
# console handler (ch)
ch = log.StreamHandler()
ch.setLevel(log.INFO)
# create format
formatter = log.Formatter('%(asctime)s %(levelname)s: %(message)s',
                                datefmt='%Y-%m-%d %I:%M:%S')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add fh & ch
log.addHandler(fh)
log.addHandler(ch)
"""

log = LogClass()
#log = log.getlog('eGoPP')


# logger
log.logger().info('eGoPreProcessing started!')


#Database connection default(reiners_db)
con = db_session()
#con.close() <--- call at file end


"""
# logger
log.info(os.environ['PGDATABASE'] + " on "
    + os.environ['PGUSER'] + "@" 
    + os.environ['PGHOST'] + ":" 
    + os.environ['PGPORT'] )
"""

"""
# log static
log.logger().info('username' + " on "
    + 'database' + "@"
    + 'host' + ":"
    + 'port')

"""

# logger -> config file = 'db_io_config.ini' (current folder)
log.logger().info(cfg.get(config_section, 'username') + " on "
    + cfg.get(config_section, 'database') + "@"
    + (cfg.get(config_section, 'host') + ":"
    + (cfg.get(config_section, 'port'))))


# create download folder
download_folder = r'C:/eGoPP/vg250/'
if not os.path.exists(download_folder):
    os.makedirs(download_folder)
    log.logger().info("Create folder: '{}'".format(download_folder))


# define files for download
download_url = 'http://www.geodatenzentrum.de/auftrag1/archiv/vektor/vg250_ebenen/'
download_file_start = 'vg250_'
download_file_end = '-01-01.gk3.shape.ebenen.zip'
years = range(2016, 2018)
log.logger().info("Download from: '{}'".format(download_url))


# download to folder and unzip
for year in years:
    # download
    file_name = download_file_start + '{}'.format(year) + download_file_end
    log.logger().info("Download: " + file_name)
    url = download_url + '{}'.format(year) + "/" + file_name
    to_path = download_folder + file_name
    #download
    #urllib.request.urlretrieve (url, to_path)
    log.logger().info("Into: " + to_path)

    # unzip
    zip = zipfile.ZipFile(to_path)
    zip.extractall(download_folder + file_name[:-4])
    log.logger().info("Unzip: " + file_name)


# logger time
log.logger().info('Downloads successfully executed in {:.2f} seconds!'.format(
        time.time() - total_time))


# load shapefiles

""" moved to db_manipulate.py
full_dir = os.walk(download_folder)
shapefile_list = []
for dirpaths, dirnames, files in full_dir:
    for file_ in files:
        if file_[-3:] == 'shp':
            # path
            shapefile_path = os.path.join(dirpaths, file_)
            log.logger().info("Shapefile path: " + shapefile_path)

            # extract date from string
            s = dirpaths.replace('\\'," ").replace('\v',' ')
            print(s)
            remove1 = [':','/','\\','_','.']
            for char in remove1:
                s = s.replace(char," ")
            remove2 = ['C','vg250','g250','ebenen','gk3','eGoPP','shape','historisch','de0001','de0101','de0201','de0301','de0401','de0501','de0601','de0701','de0801','de0901','de1001','de1101',' ','mv','kreisreform',' ']
            for char in remove2:
                s = s.replace(char,"")
            clean_str = s[:-10]
            print(clean_str)
            date_str = dparser.parse(clean_str,fuzzy=True).date()

            # table
            table_name = os.path.join(file_)[:-4] + "_" + date_str.strftime('%Y-%m-%d')
            log.logger().info("Table name: " + table_name)
            entry = []
            entry.append(shapefile_path)
            entry.append(table_name)
            shapefile_list.append(entry)

log.logger().info("Shapefile list: '{}'".format(shapefile_list))
"""



""" Upload to database using shp2pgsql
# execute
for shape_path, table_name in shapefile_list:
    cmd = 'shp2pgsql "' + shape_path + '" boundaries.' + table_name + ' | psql > NUL'
    log.logger().info("Execute: " + cmd)
    subprocess.check_call(cmd, shell=True)

log.logger().info("Imported tables: '{}'".format([i[1] for i in shapefile_list]))
"""

# logger time
log.logger().info('eGoPreProcessing successfully executed in {:.2f} seconds!'.format(
        time.time() - total_time))


# stop logger
log.logger().info("Stop log")
log.stop_log_fhch()
""" moved to db_log fnc stop_log_fhch
log.removeHandler(fh)
log.removeHandler(ch)
fh.close()
ch.close()
"""

#close DB connection/ Drop prostgresql obj.
con.close()

# -*- coding: utf-8 -*-

"""
Service functions for reeem_db

This file is part of project OEDB (https://github.com/OpenEnergyPlatform).
It's copyrighted by the contributors recorded in the version control history:
#!!

SPDX-License-Identifier: AGPL-3.0-or-later
"""

__copyright__ = "© Reiner Lemoine Institut"
__license__ = "GNU Affero General Public License Version 3 (AGPL-3.0)"
__license_url__ = "https://www.gnu.org/licenses/agpl-3.0.en.html"
__author__ = "jh-RLI"
__version__ = "v0.1.0"

import sys
import os
import time
import getpass
import logging
from sqlalchemy import *
import configparser as cp
import pandas as pd
from db_logger import *

# parameter
config_file = 'db_io_config.ini'
config_section = 'reiners_db'
log_file = 'db_adapter.log'
sys.tracebacklimit = 0
cfg = cp.RawConfigParser()

"""
moved to ---> db_logger.py
def logger():
   Configure logging in console and log file.
    
    Returns
    -------
    rl : logger
        Logging in console (ch) and file (fh).

    # set root logger (rl)
    rl = logging.getLogger('DBLogger')
    rl.setLevel(logging.INFO)
    rl.propagate = False

    # set format
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')

    # console handler (ch)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    rl.addHandler(ch)

    # file handler (fh)
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    rl.addHandler(fh)

    return rl
"""

def config_section_set(key, value):
    """Create a config file.

    Sets input values to a [db_section] key - pair.

    Parameters
    ----------
    key : str
        The username.
    value : str
        The pw.

    """

    with open(config_file, 'w') as config:  # save
        if not cfg.has_section(config_section):
            cfg.add_section(config_section)
            cfg.set(config_section, 'username', key)
            cfg.set(config_section, 'database', config_section)
            cfg.set(config_section, 'host', '130.XXX.XX.XX')
            cfg.set(config_section, 'port', port)
            cfg.set(config_section, 'password', value)
            cfg.write(config)


def config_file_load():
    """Load the username and pw from config file."""

    if os.path.isfile(config_file):
        config_file_init()
    else:
        config_file_not_found_message()


def config_file_init():
    """Read config file."""

    try:
        print('Load ' + config_file)
        cfg.read(config_file)
        global _loaded
        _loaded = True
    except FileNotFoundError:
        config_file_not_found_message()


def config_file_get(key):
    """Read data from config file.

    Parameters
    ----------
    key : str
        Config entries.
    """

    if not _loaded:
        config_file_init()
    try:
        return cfg.getfloat(config_section, key)
    except Exception:
        try:
            return cfg.getint(config_section, key)
        except:
            try:
                return cfg.getboolean(config_section, key)
            except:
                return cfg.get(config_section, key)


def config_file_not_found_message():
    """Show error message if file not found."""

    print('The config file {} could not be found!'.format(config_file))


def db_session():
    """SQLAlchemy session object with valid connection to database

    Returns
    -------
    conn : SQLAlchemy object
        Database connection object.
    """

    # host = input('host (default 192.168.10.25): ')
    host = '192.168.10.25'
    # print('host: ' + host)

    # port = input('port (default 5432): ')
    global port
    port = '5432'
    # print('port: ' + port)

    # database = input("database name (default 'reiners_db'): ")
    database = config_section
    # print('database: ' + database)

    #listlog = [host, port, database]

    # user = ''
    try:
        config_file_load()
        user = config_file_get('username')
        print('Hello ' + user + '!')
    except:
        print('Please provide connection parameters!')
        user = input('User name (default surname_name): ')

    # password = ''
    try:
        password = config_file_get('password')
    except:
        password = getpass.getpass(prompt='Password: ',
                                   stream=sys.stderr)
        config_section_set(key=user, value=password)
        print('Config file created!')

    # engine
    try:
        conn = create_engine(
            'postgresql://' + '%s:%s@%s:%s/%s' % (user,
                                                  password,
                                                  host,
                                                  port,
                                                  database)).connect()
    except:
        print('Password authentication failed for user "{}"'.format(user))
        try:
            os.remove(config_file)
            print('Existing config file deleted! '
                  'Restart script and try again!')
        except OSError:
            print(
                'Cannot delete file. '
                'Please check login parameters in config file!')

    print('Database connection established!')
    return conn



""" moved to ---> db_logger
def scenario_log(con, project, version, io, schema, table, script, comment):
 
    Write an entry in scenario log table.

    Parameters
    ----------
    con : connection
        SQLAlchemy connection object.
    project : str
        Project name.
    version : str
        Version number.
    io : str
        IO-type (input, output, temp).
    schema : str
        Database schema.
    table : str
        Database table.
    script : str
        Script name.
    comment : str
        Comment.

    """



def reeem_filenamesplit(filename):
    """file name identification"""

    filenamesplit = filename.replace(".xlsx", "").replace(".csv", "").split("_")
    fns = {}
    fns['day'] = filenamesplit[0]
    fns['pathway'] = filenamesplit[1]
    fns['model'] = filenamesplit[2]
    fns['framework'] = filenamesplit[3]
    fns['version'] = filenamesplit[4]
    fns['io'] = filenamesplit[5]
    return fns
    


    # import pprint
    # pprint.pprint(fns)

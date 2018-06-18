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
# import time
import getpass
# import logging
import sqlalchemy
from configparser import ConfigParser
# import pandas as pd
# from db_logger import *

# parameter
CONFIG_FILENAME = 'db_io_config.ini'
CONFIG_SECTION = 'reiners_db'

LOG_FILENAME = 'db_adapter.log'

sys.tracebacklimit = 0

cfg = ConfigParser()

_loaded = False


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

    with open(CONFIG_FILENAME, 'w') as config:  # save
        if not cfg.has_section(CONFIG_SECTION):
            cfg.add_section(CONFIG_SECTION)
            cfg.set(CONFIG_SECTION, 'username', key)
            cfg.set(CONFIG_SECTION, 'database', CONFIG_SECTION)
            cfg.set(CONFIG_SECTION, 'host', '130.XXX.XX.XX')
            cfg.set(CONFIG_SECTION, 'port', '5432')
            cfg.set(CONFIG_SECTION, 'password', value)
            cfg.write(config)


def config_file_init():
    """Read config file."""

    try:
        cfg.read(CONFIG_FILENAME)
        global _loaded
        _loaded = True
    except FileNotFoundError:
        raise FileNotFoundError(
            'The config file {} could not be found!'.format(CONFIG_FILENAME))


def db_session():
    """SQLAlchemy session object with valid connection to database

    Returns
    -------
    conn : SQLAlchemy object
        Database connection object.
    """
    # listlog = [host, port, database]

    config_file_init()

    database = CONFIG_SECTION
    host = cfg[CONFIG_SECTION].get('host', '192.168.10.25')
    port = cfg[CONFIG_SECTION].get('port', '5432')

    # user = ''
    try:
        user = cfg[CONFIG_SECTION]['username']
        print('Hello ' + user + '!')
    except KeyError:
        print('Please provide connection parameters!')
        user = input('User name (default surname_name): ')

    # password = ''
    try:
        password = cfg[CONFIG_SECTION]['password']
    except KeyError:
        password = getpass.getpass(
            stream=sys.stderr
        )

    # engine
    credentials = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    conn = sqlalchemy.create_engine(credentials)
    conn.connect()
    return conn


def reeem_filenamesplit(filename):
    """file name identification"""

    filenamesplit = (
        filename.replace(".xlsx", "").replace(".csv", "").split("_"))
    fns = {
        'day': filenamesplit[0],
        'pathway': filenamesplit[1],
        'model': filenamesplit[2],
        'framework': filenamesplit[3],
        'version': filenamesplit[4],
        'io': filenamesplit[5],
    }
    return fns

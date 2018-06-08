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



import logging


# parameter
log_file = 'db_adapter.log'

class LogClass:
    """Class to create a LogClass instance witch makes it easy to use the Log
        with different skripts

        Maybe add input values to make the Log more dynamic


        Parameters
        -------
    """


    def logger(self):
        """Configure logging in console and log file.

        Returns
        -------
        logger : logger
            Logging in console (ch) and file (fh).

        old code
        -------
        # set root logger (rl)
        rl = logging.getLogger('eGoPP')
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
        """

        # configure logging
        logger = logging.getLogger('eGoPP')
        logger.setLevel(logging.INFO)
        # file handler (fh)
        fh = logging.FileHandler(r'C:/eGoPP/ego_pp.log')
        fh.setLevel(logging.INFO)
        # console handler (ch)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        # create format
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s',
                                      datefmt='%Y-%m-%d %I:%M:%S')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add fh & ch
        logger.addHandler(fh)
        logger.addHandler(ch)

        return logger


    def stop_log_fhch(self):
        """ Terminate the file handler (fh) and console handler (ch)

            Parameters
            ----------

        """

        # stop logging
        self.logger().logger.removeHandler(self.logger().fh)
        self.logger().logger.removeHandler(self.logger().ch)
        self.logger().fh.close()
        self.logger().ch.close()



def scenario_log(con, project, version, io, schema, table, script, comment):
    """Write an entry in scenario log table.

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
    
    
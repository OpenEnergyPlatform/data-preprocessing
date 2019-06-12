#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
OEP MaStR Processing

Read data from MaStR API, process, and write to file and OEP
The data will be downloaded to the folder /data.

SPDX-License-Identifier: AGPL-3.0-or-later
"""

__copyright__ = "© Reiner Lemoine Institut"
__license__ = "GNU Affero General Public License Version 3 (AGPL-3.0)"
__url__ = "https://www.gnu.org/licenses/agpl-3.0.en.html"
__author__ = "Ludee; christian-rli"
__issue__ = "https://github.com/OpenEnergyPlatform/examples/issues/52"
__version__ = "v0.7.0"

from config import setup_logger
from mastr_power_unit_download import download_power_unit
from mastr_wind_download import download_unit_wind, download_unit_wind_eeg
from mastr_wind_process import make_wind
from mastr_hydro_download import download_unit_hydro, download_unit_hydro_eeg
from mastr_hydro_process import make_hydro
from mastr_biomass_download import download_unit_biomass, download_unit_biomass_eeg
from mastr_biomass_process import make_biomass
from mastr_solar_download import download_unit_solar, download_unit_solar_eeg
from mastr_solar_process import make_solar

import time

"""version"""
DATA_VERSION = 'rli_v1.3.1'

if __name__ == "__main__":
    """logging"""
    log = setup_logger()
    start_time = time.time()
    log.info(f'MaStR script started with data version: {DATA_VERSION}')

    """OEP"""
    # metadata = oep_session()

    """MaStR Einheiten"""
    download_power_unit()

    """Wind"""
    # download_unit_wind()
    # download_unit_wind_eeg()
    # make_wind()

    """Hydro"""
    # download_unit_hydro()
    # download_unit_hydro_eeg()
    # make_hydro()

    """Biomass"""
    # download_unit_biomass()
    # download_unit_biomass_eeg()
    # make_biomass()

    """Solar"""
    # download_unit_solar()
    # download_unit_solar_eeg()
    # make_solar()

    """close"""
    log.info('MaSTR script successfully executed in {:.2f} seconds'
             .format(time.time() - start_time))

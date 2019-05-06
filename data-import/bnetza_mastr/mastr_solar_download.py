#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
BNetzA - MaStR Download - Solar

Read data from MaStR API and write to CSV files.

SPDX-License-Identifier: AGPL-3.0-or-later
"""

__copyright__ = "© Reiner Lemoine Institut"
__license__ = "GNU Affero General Public License Version 3 (AGPL-3.0)"
__url__ = "https://www.gnu.org/licenses/agpl-3.0.en.html"
__author__ = "Ludee; christian-rli"
__issue__ = "https://github.com/OpenEnergyPlatform/examples/issues/52"
__version__ = "v0.7.0"

from config import get_data_version, write_to_csv
from sessions import mastr_session
from mastr_power_unit_download import read_power_units

import pandas as pd
from multiprocessing import Process, Lock
import numpy as np
import datetime
import os
from zeep.helpers import serialize_object

import logging

log = logging.getLogger(__name__)

"""SOAP API"""
client, client_bind, token, user = mastr_session()
api_key = token
my_mastr = user


def get_power_unit_solar(mastr_unit_solar):
    """Get Solareinheit from API using GetEinheitSolar.

    Parameters
    ----------
    mastr_unit_solar : object
        Solar from EinheitMastrNummerId.

    Returns
    -------
    unit_solar : DataFrame
        Solareinheit.
    """
    data_version = get_data_version()
    c = client_bind.GetEinheitSolar(apiKey=api_key,
                                    marktakteurMastrNummer=my_mastr,
                                    einheitMastrNummer=mastr_unit_solar)
    s = serialize_object(c)
    df = pd.DataFrame(list(s.items()), )
    unit_solar = df.set_index(list(df.columns.values)[0]).transpose()
    unit_solar.reset_index()
    unit_solar.index.names = ['lid']
    unit_solar['version'] = data_version
    unit_solar['timestamp'] = str(datetime.datetime.now())
    return unit_solar


def read_unit_solar(csv_name):
    """Read Solareinheit from CSV file.

    Parameters
    ----------
    csv_name : str
        Name of file.

    Returns
    -------
    unit_solar : DataFrame
        Solareinheit.
    """
    # log.info(f'Read data from {csv_name}')
    unit_solar = pd.read_csv(csv_name, header=0, encoding='utf-8', sep=';', index_col=False,
                             dtype={'lid': int,
                                    'Ergebniscode': str,
                                    'AufrufVeraltet': str,
                                    'AufrufLebenszeitEnde': str,
                                    'AufrufVersion': str,
                                    'EinheitMastrNummer': str,
                                    'DatumLetzteAktualisierung': str,
                                    'LokationMastrNummer': str,
                                    'NetzbetreiberpruefungStatus': str,
                                    'NetzbetreiberpruefungDatum': str,
                                    'AnlagenbetreiberMastrNummer': str,
                                    'Land': str,
                                    'Bundesland': str,
                                    'Landkreis': str,
                                    'Gemeinde': str,
                                    'Gemeindeschluessel': str,
                                    'Postleitzahl': str,
                                    'Gemarkung': str,
                                    'FlurFlurstuecknummern': str,
                                    'Strasse': str,
                                    'StrasseNichtGefunden': str,
                                    'Hausnummer': str,
                                    'HausnummerNichtGefunden': str,
                                    'Adresszusatz': str,
                                    'Ort': str,
                                    'Laengengrad': str,
                                    'Breitengrad': str,
                                    'UtmZonenwert': str,
                                    'UtmEast': str,
                                    'UtmNorth': str,
                                    'GaussKruegerHoch': str,
                                    'GaussKruegerRechts': str,
                                    'Meldedatum': str,
                                    'GeplantesInbetriebnahmedatum': str,
                                    'Inbetriebnahmedatum': str,
                                    'DatumEndgueltigeStilllegung': str,
                                    'DatumBeginnVoruebergehendeStilllegung': str,
                                    'DatumWiederaufnahmeBetrieb': str,
                                    'EinheitBetriebsstatus': str,
                                    'BestandsanlageMastrNummer': str,
                                    'NichtVorhandenInMigriertenEinheiten': str,
                                    'NameStromerzeugungseinheit': str,
                                    'Weic': str,
                                    'WeicDisplayName': str,
                                    'Kraftwerksnummer': str,
                                    'Energietraeger': str,
                                    'Bruttoleistung': float,
                                    'Nettonennleistung': float,
                                    'AnschlussAnHoechstOderHochSpannung': str,
                                    'Schwarzstartfaehigkeit': str,
                                    'Inselbetriebsfaehigkeit': str,
                                    'Einsatzverantwortlicher': str,
                                    'FernsteuerbarkeitNb': str,
                                    'FernsteuerbarkeitDv': str,
                                    'FernsteuerbarkeitDr': str,
                                    'Einspeisungsart': str,
                                    'PraequalifiziertFuerRegelenergie': str,
                                    'GenMastrNummer': str,
                                    'zugeordneteWirkleistungWechselrichter': str,
                                    'GemeinsamerWechselrichterMitSpeicher': str,
                                    'AnzahlModule': str,
                                    'Lage': str,
                                    'Leistungsbegrenzung': str,
                                    'EinheitlicheAusrichtungUndNeigungswinkel': str,
                                    'Hauptausrichtung': str,
                                    'HauptausrichtungNeigungswinkel': str,
                                    'Nebenausrichtung': str,
                                    'NebenausrichtungNeigungswinkel': str,
                                    'InAnspruchGenommeneFlaeche': str,
                                    'ArtDerFlaeche': str,
                                    'InAnspruchGenommeneAckerflaeche': str,
                                    'Nutzungsbereich': str,
                                    'EegMastrNummer': str,
                                    'version': str,
                                    'timestamp': str})
    # log.info(f'Finished reading data from {csv_name}')
    return unit_solar


def get_unit_solar_eeg(mastr_solar_eeg):
    """Get EEG-Anlage-Solar from API using GetAnlageEegSolar.

    Parameters
    ----------
    mastr_solar_eeg : str
        MaStR EEG Nr.

    Returns
    -------
    unit_solar_eeg : DataFrame
        EEG-Anlage-Solar.
    """
    data_version = get_data_version()
    c = client_bind.GetAnlageEegSolar(apiKey=api_key,
                                      marktakteurMastrNummer=my_mastr,
                                      eegMastrNummer=mastr_solar_eeg)
    s = serialize_object(c)
    df = pd.DataFrame(list(s.items()), )
    unit_solar_eeg = df.set_index(list(df.columns.values)[0]).transpose()
    unit_solar_eeg.reset_index()
    unit_solar_eeg.index.names = ['lid']
    unit_solar_eeg["version"] = data_version
    unit_solar_eeg["timestamp"] = str(datetime.datetime.now())
    return unit_solar_eeg


def read_unit_solar_eeg(csv_name):
    """
    Encode and read EEG-Anlage-Solar from CSV file.

    Parameters
    ----------
    csv_name : str
        Name of file.

    Returns
    -------
    unit_solar_eeg : DataFrame
        EEG-Anlage-Solar
    """
    # log.info(f'Read data from {csv_name}')
    unit_solar_eeg = pd.read_csv(csv_name, header=0, sep=';', index_col=False, encoding='utf-8',
                                 dtype={'lid': int,
                                        'Ergebniscode': str,
                                        'AufrufVeraltet': str,
                                        'AufrufLebenszeitEnde': str,
                                        'AufrufVersion': str,
                                        'Meldedatum': str,
                                        'DatumLetzteAktualisierung': str,
                                        'EegInbetriebnahmedatum': str,
                                        'EegMastrNummer': str,
                                        'InanspruchnahmeZahlungNachEeg': str,
                                        'AnlagenschluesselEeg': str,
                                        'AnlagenkennzifferAnlagenregister': str,
                                        'InstallierteLeistung': str,
                                        'RegistrierungsnummerPvMeldeportal': str,
                                        'MieterstromZugeordnet': str,
                                        'MieterstromMeldedatum': str,
                                        'MieterstromErsteZuordnungZuschlag': str,
                                        'AusschreibungZuschlag': str,
                                        'ZugeordneteGebotsmenge': str,
                                        'Zuschlagsnummer': str,
                                        'AnlageBetriebsstatus': str,
                                        'VerknuepfteEinheit': str,
                                        'version': str,
                                        'timestamp': str})
    # log.info(f'Finished reading data from {csv_name}')
    return unit_solar_eeg


def setup_power_unit_solar():
    """Setup file for Stromerzeugungseinheit-Solar.

    Check if file with Stromerzeugungseinheit-Solar exists. Create if not exists.
    Load Stromerzeugungseinheit-Solar from file if exists.

    Returns
    -------
    power_unit_solar : DataFrame
        Stromerzeugungseinheit-Solar.
    """
    data_version = get_data_version()
    csv_see = f'data/bnetza_mastr_{data_version}_power-unit.csv'
    csv_see_solar = f'data/bnetza_mastr_{data_version}_power-unit-solar.csv'
    if not os.path.isfile(csv_see_solar):
        power_unit = read_power_units(csv_see)
        power_unit = power_unit.drop_duplicates()
        power_unit_solar = power_unit[power_unit.Einheittyp == 'Solareinheit']
        power_unit_solar.index.names = ['see_id']
        power_unit_solar.reset_index()
        power_unit_solar.index.names = ['id']
        # log.info(f'Write data to {csv_see_solar}')
        write_to_csv(csv_see_solar, power_unit_solar)
        return power_unit_solar
    else:
        power_unit_solar = read_power_units(csv_see_solar)
        # log.info(f'Read data from {csv_see_solar}')
        return power_unit_solar


def download_single_unit_solar(unit_solar_entry, csv_solar, lock):
    """Download single Solareinheit entry and write its content in a file.

    :param unit_solar_entry: single entry from a unit_solar_list
    :param csv_solar: file in which to write the content of the unit_solar_entry
    :param lock: instance of Lock to prevent simultaneous write access to csv_solar file
    """
    lock.acquire()
    try:
        unit_solar = get_power_unit_solar(unit_solar_entry)
        write_to_csv(csv_solar, unit_solar)
    finally:
        lock.release()


def download_unit_solar():
    """Download Solareinheit.

    Existing units: 31543 (2019-02-10)
    """
    start_from = 36154

    data_version = get_data_version()
    csv_solar = f'data/bnetza_mastr_{data_version}_unit-solar.csv'
    unit_solar = setup_power_unit_solar()
    unit_solar_list = unit_solar['EinheitMastrNummer'].values.tolist()
    unit_solar_list_len = len(unit_solar_list)
    log.info(f'Download MaStR Solar')
    log.info(f'Number of unit_solar: {unit_solar_list_len}')

    lock = Lock()
    for i in range(start_from, unit_solar_list_len, 1):
        single_dl = Process(
            target=download_single_unit_solar,
            args=(unit_solar_list[i], csv_solar, lock)
        )
        single_dl.start()


def download_single_unit_solar_eeg(unit_solar_entry, csv_solar_eeg, lock):
    """Download single unit_solar_eeg entry and write its content in a file.

    :param unit_solar_entry: single entry from a unit_solar_list
    :param csv_solar_eeg: file in which to write the content of the unit_solar_entry
    :param lock: instance of Lock to prevent simultaneous write access to csv_solar file
    """
    lock.acquire()
    try:
        unit_solar_eeg = get_unit_solar_eeg(unit_solar_entry)
        write_to_csv(csv_solar_eeg, unit_solar_eeg)
    finally:
        lock.release()


def download_unit_solar_eeg():
    """Download unit_solar_eeg using GetAnlageEegSolar request."""
    data_version = get_data_version()
    csv_solar_eeg = f'data/bnetza_mastr_{data_version}_unit-solar-eeg.csv'
    unit_solar = setup_power_unit_solar()

    unit_solar_list = unit_solar['EegMastrNummer'].values.tolist()
    unit_solar_list_len = len(unit_solar_list)

    lock = Lock()
    for i in range(0, unit_solar_list_len, 1):
        single_dl = Process(
            target=download_single_unit_solar_eeg,
            args=(unit_solar_list[i], csv_solar_eeg, lock)
        )
        single_dl.start()

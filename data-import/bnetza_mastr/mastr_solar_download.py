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
from zeep.exceptions import Fault
import multiprocessing as mp
from multiprocessing import queues
import logging
import time

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


def download_proc(queue, idx, writing_queue, api_call, entry_descr=''):
    """Execute the download from the queue"""
    pr = mp.current_process()
    rstart = time.time()
    print('Start {} from loop {}, queue empty={}'.format(pr.pid, idx, str(queue.empty())))
    while not queue.empty():
        unit_entry = queue.get()  # Read from the queue and do nothing
        try:
            df = api_call(unit_entry)
            writing_queue.put(df)
        except Fault:
            log.error('Downloading {} failed : ({})'.format(entry_descr, unit_entry))
    print('Finish {} from loop {} in {}s'.format(pr.pid, idx, time.time() - rstart))


def download_solar_proc(queue, idx, writing_queue):
    """Execute the download from the queue"""
    download_proc(queue, idx, writing_queue, get_power_unit_solar, 'unit_solar')


def download_solar_eeg_proc(queue, idx, writing_queue):
    """Execute the download from the queue"""
    download_proc(queue, idx, writing_queue, get_unit_solar_eeg, 'unit_solar_egg')


def download_unit_solar(n_entries=None, start_from=0):
    """Download Solareinheit.

    :param n_entries: number of entries from unit_solar_list
    :param start_from: index of first unit_solar_entry in the unit_solar_list
    Existing units: 31543 (2019-02-10)
    """

    data_version = get_data_version()
    csv_solar = f'data/bnetza_mastr_{data_version}_unit-solar.csv'
    unit_solar = setup_power_unit_solar()
    unit_solar_list = unit_solar['EinheitMastrNummer'].values.tolist()
    unit_solar_list_len = len(unit_solar_list)
    log.info(f'Download MaStR Solar')
    log.info(f'Number of unit_solar: {unit_solar_list_len}')

    if n_entries is None:
        n_entries = len(unit_solar_list)

    parallel_download(
        csv_solar,
        unit_solar_list,
        download_solar_proc,
        n_entries=n_entries,
        start_from=start_from
    )


def download_unit_solar_eeg(n_entries=None, start_from=0):
    """Download unit_solar_eeg using GetAnlageEegSolar request.

    :param n_entries: number of entries from unit_solar_list
    :param start_from: index of first unit_solar_entry in the unit_solar_list
    """
    data_version = get_data_version()
    csv_solar_eeg = f'data/bnetza_mastr_{data_version}_unit-solar-eeg.csv'
    unit_solar = setup_power_unit_solar()

    unit_solar_list = unit_solar['EegMastrNummer'].values.tolist()

    if n_entries is None:
        n_entries = len(unit_solar_list)

    parallel_download(
        csv_solar_eeg,
        unit_solar_list,
        download_solar_eeg_proc,
        n_entries=n_entries,
        start_from=start_from
    )


def load_data(entries, queue):
    """Load entries in a queue."""
    lstart = time.time()
    print('Loading..  {} entries in the queue'.format(len(entries)))
    for entry in entries:
        queue.put(entry)
    print('Loaded {} entries in the queue in {}s'.format(len(entries), time.time() - lstart))


def writer_proc(queue, n_entries, csv_file):
    """Process responsible to write data in a queue to a csv file"""
    pr = mp.current_process()
    print('{} from writer, queue empty={}'.format(pr.pid, str(queue.empty())))
    wstart = time.time()

    n_iter_before_save = np.min([int(n_entries / 10.), 20000])

    n_loop = 0
    df_list = []
    while n_loop < n_entries:
        try:
            df = queue.get(timeout=3)  # Read from the queue and do nothing
            df_list.append(df)
        except queues.Empty:
            print('End of queue')
            print('{} Write to file {}'.format(time.ctime(time.time()), n_loop))
            if df_list:
                write_to_csv(csv_file, pd.concat(df_list))
                df_list = []
        if np.mod(n_loop, n_iter_before_save) == 0:
            print('{} Write to file {}'.format(time.ctime(time.time()), n_loop))
            write_to_csv(csv_file, pd.concat(df_list))
            df_list = []
        n_loop = n_loop + 1
    if df_list:
        print('{} Write to file {}'.format(time.ctime(time.time()), n_loop))
        write_to_csv(csv_file, pd.concat(df_list))
    print('{} writer done in {}s'.format(pr.pid, time.time() - wstart))


def parallel_download(csv_file, entries_list, dl_proc, n_entries=60, start_from=0):

    print('Files to download: {}, starting from idx {} in the entry list'.format(
        n_entries,
        start_from)
    )

    num_cpu = mp.cpu_count()
    write_queue = mp.Queue()
    # Queues for download entries
    pqueues = []
    download_ps = []

    for i in range(num_cpu):
        pqueue = mp.Queue()  # writer() writes to pqueue from _this_ process
        pqueues.append(pqueue)
        download_p = mp.Process(target=dl_proc, args=((pqueue), (i), (write_queue),))
        download_p.daemon = True
        download_ps.append(download_p)

    _start = time.time()

    tot_entries_in_list = len(entries_list)
    # make sure the user demand do not query indexes beyond the entries list max size
    if start_from + n_entries >= tot_entries_in_list:
        n_entries = tot_entries_in_list - start_from

    solar_idxs = []
    if n_entries > 0:
        # split the number of entries equally between the different download queues
        step = n_entries / num_cpu
        step = np.int(step)

        for i in range(num_cpu):
            solar_idxs.append([start_from + i * step, start_from + (i + 1) * step])
        solar_idxs[-1][1] = start_from + n_entries

    # load the entries in the download queues
    for idxs, j in zip(solar_idxs, range(num_cpu)):
        load_data(entries_list[idxs[0]:idxs[1]], pqueues[j])
        download_ps[j].start()

    # start the process which write to csv file from a queue
    time.sleep(1)
    writer_p = mp.Process(target=writer_proc, args=((write_queue), (n_entries), (csv_file)))
    writer_p.daemon = True

    time.sleep(2)
    writer_p.start()
    writer_p.join()

    print("Total process took {} seconds".format(time.time() - _start))


if __name__ == '__main__':
    download_unit_solar(n_entries=10, start_from=236154)

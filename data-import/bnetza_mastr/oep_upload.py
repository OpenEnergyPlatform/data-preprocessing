#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Upload to OEP

Read data from CSV, write to OEP

SPDX-License-Identifier: AGPL-3.0-or-later
"""

__copyright__ = "© Reiner Lemoine Institut"
__license__ = "GNU Affero General Public License Version 3 (AGPL-3.0)"
__url__ = "https://www.gnu.org/licenses/agpl-3.0.en.html"
__author__ = "Ludee"
__issue__ = "https://github.com/OpenEnergyPlatform/examples/issues/52"
__version__ = "v0.7.0"

import config as lc

# import getpass
import os
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
import oedialect
from collections import namedtuple
from config import get_data_version
import pandas as pd


UserToken = namedtuple('UserToken', ['user', 'token'])

import logging
log = logging.getLogger(__name__)


def oep_config():
    """Access config.ini.

    Returns
    -------
    UserToken : namedtuple
        API token (key) and user name (value).
    """
    config_section = 'OEP'

    # username
    try:
        lc.config_file_load()
        user = lc.config_file_get(config_section, 'user')
        log.info(f'Hello {user}, welcome back')
    except FileNotFoundError:
        user = input('Please provide your OEP username (default surname_name):')
        log.info(f'Hello {user}')

    # token
    try:
        token = lc.config_file_get(config_section, 'token')
        print(f'Load API token')
    except:
        import sys
        token = input('Token:')
        # token = getpass.getpass(prompt = 'Token:',
        #                         stream = sys.stdin)
        lc.config_section_set(config_section, value=user, key=token)
        log.info('Config file created')
    return UserToken(user, token)


# a = oep_config()
# a.user
# a.token

def oep_session():
    """SQLAlchemy session object with valid connection to database.

    Returns
    -------
    metadata : SQLAlchemy object
        Database connection object.
    """
    user, token = oep_config()
    # user = input('Enter OEP-username:')
    # token = getpass.getpass('Token:')

    # engine
    try:
        oep_url = 'openenergy-platform.org'  # 'oep.iks.cs.ovgu.de'
        oed_string = f'postgresql+oedialect://{user}:{token}@{oep_url}'
        engine = sa.create_engine(oed_string)
        metadata = sa.MetaData(bind=engine)

        print(f'Connect to OEP: {engine}')
        return engine, metadata

    except:
        print('Password authentication failed for user: "{}"'.format(user))
        try:
            os.remove(lc.config_file)
            print('Existing config file deleted! /n Restart script and try again!')
        except OSError:
            print('Cannot delete file! /n Please check login parameters in config file!')


def oep_create_mastr_wind():
    """Create table for MaStR Wind

    """
    table_name_wind = 'bnetza_mastr_wind'
    schema_name = 'sandbox'
    engine, metadata = oep_session()

    MastrWind = sa.Table(
        table_name_wind,
        metadata,
        sa.Column('wind_id', sa.INTEGER),
        sa.Column('id', sa.INTEGER),
        sa.Column('lid', sa.INTEGER),
        sa.Column('EinheitMastrNummer', sa.VARCHAR(50)),
        sa.Column('Name', sa.VARCHAR(50)),
        sa.Column('Einheitart', sa.VARCHAR(50)),
        sa.Column('Einheittyp', sa.VARCHAR(50)),
        sa.Column('Standort', sa.VARCHAR(50)),
        sa.Column('Bruttoleistung', sa.Float),
        sa.Column('Erzeugungsleistung', sa.Float),
        sa.Column('EinheitBetriebsstatus', sa.VARCHAR(50)),
        sa.Column('Anlagenbetreiber', sa.VARCHAR(50)),
        sa.Column('EegMastrNummer', sa.VARCHAR(50)),
        sa.Column('KwkMastrNummer', sa.VARCHAR(50)),
        sa.Column('SpeMastrNummer', sa.VARCHAR(50)),
        sa.Column('GenMastrNummer', sa.VARCHAR(50)),
        sa.Column('BestandsanlageMastrNummer', sa.VARCHAR(50)),
        sa.Column('NichtVorhandenInMigriertenEinheiten', sa.VARCHAR(50)),
        sa.Column('StatisikFlag', sa.VARCHAR(50)),
        sa.Column('version', sa.VARCHAR(50)),
        sa.Column('timestamp', sa.VARCHAR(50)),
        sa.Column('lid_w', sa.VARCHAR(50)),
        sa.Column('Ergebniscode', sa.VARCHAR(50)),
        sa.Column('AufrufVeraltet', sa.VARCHAR(50)),
        sa.Column('AufrufLebenszeitEnde', sa.VARCHAR(50)),
        sa.Column('AufrufVersion', sa.VARCHAR(50)),
        sa.Column('DatumLetzteAktualisierung', sa.VARCHAR(50)),
        sa.Column('LokationMastrNummer', sa.VARCHAR(50)),
        sa.Column('NetzbetreiberpruefungStatus', sa.VARCHAR(50)),
        sa.Column('NetzbetreiberpruefungDatum', sa.VARCHAR(50)),
        sa.Column('AnlagenbetreiberMastrNummer', sa.VARCHAR(50)),
        sa.Column('Land', sa.VARCHAR(50)),
        sa.Column('Bundesland', sa.VARCHAR(50)),
        sa.Column('Landkreis', sa.VARCHAR(50)),
        sa.Column('Gemeinde', sa.VARCHAR(50)),
        sa.Column('Gemeindeschluessel', sa.VARCHAR(50)),
        sa.Column('Postleitzahl', sa.VARCHAR(5)),
        sa.Column('Gemarkung', sa.VARCHAR(50)),
        sa.Column('FlurFlurstuecknummern', sa.VARCHAR(50)),
        sa.Column('Strasse', sa.VARCHAR(50)),
        sa.Column('StrasseNichtGefunden', sa.VARCHAR(50)),
        sa.Column('Hausnummer', sa.VARCHAR(50)),
        sa.Column('HausnummerNichtGefunden', sa.VARCHAR(50)),
        sa.Column('Adresszusatz', sa.VARCHAR(50)),
        sa.Column('Ort', sa.VARCHAR(50)),
        sa.Column('Laengengrad', sa.Float),
        sa.Column('Breitengrad', sa.Float),
        sa.Column('UtmZonenwert', sa.VARCHAR(50)),
        sa.Column('UtmEast', sa.Float),
        sa.Column('UtmNorth', sa.Float),
        sa.Column('GaussKruegerHoch', sa.Float),
        sa.Column('GaussKruegerRechts', sa.Float),
        sa.Column('Meldedatum', sa.VARCHAR(50)),
        sa.Column('GeplantesInbetriebnahmedatum', sa.VARCHAR(50)),
        sa.Column('Inbetriebnahmedatum', sa.VARCHAR(50)),
        sa.Column('DatumEndgueltigeStilllegung', sa.VARCHAR(50)),
        sa.Column('DatumBeginnVoruebergehendeStilllegung', sa.VARCHAR(50)),
        sa.Column('DatumWiederaufnahmeBetrieb', sa.VARCHAR(50)),
        sa.Column('EinheitBetriebsstatus_w', sa.VARCHAR(50)),
        sa.Column('BestandsanlageMastrNummer_w', sa.VARCHAR(50)),
        sa.Column('NichtVorhandenInMigriertenEinheiten_w', sa.VARCHAR(50)),
        sa.Column('AltAnlagenbetreiberMastrNummer', sa.VARCHAR(50)),
        sa.Column('DatumDesBetreiberwechsels', sa.VARCHAR(50)),
        sa.Column('DatumRegistrierungDesBetreiberwechsels', sa.VARCHAR(50)),
        sa.Column('StatisikFlag_w', sa.VARCHAR(50)),
        sa.Column('NameStromerzeugungseinheit', sa.VARCHAR(50)),
        sa.Column('Weic', sa.VARCHAR(50)),
        sa.Column('WeicDisplayName', sa.VARCHAR(50)),
        sa.Column('Kraftwerksnummer', sa.VARCHAR(50)),
        sa.Column('Energietraeger', sa.VARCHAR(50)),
        sa.Column('Bruttoleistung_w', sa.Float),
        sa.Column('Nettonennleistung', sa.Float),
        sa.Column('AnschlussAnHoechstOderHochSpannung', sa.VARCHAR(50)),
        sa.Column('Schwarzstartfaehigkeit', sa.VARCHAR(50)),
        sa.Column('Inselbetriebsfaehigkeit', sa.VARCHAR(50)),
        sa.Column('Einsatzverantwortlicher', sa.VARCHAR(50)),
        sa.Column('FernsteuerbarkeitNb', sa.VARCHAR(50)),
        sa.Column('FernsteuerbarkeitDv', sa.VARCHAR(50)),
        sa.Column('FernsteuerbarkeitDr', sa.VARCHAR(50)),
        sa.Column('Einspeisungsart', sa.VARCHAR(50)),
        sa.Column('PraequalifiziertFuerRegelenergie', sa.VARCHAR(50)),
        sa.Column('GenMastrNummer_w', sa.VARCHAR(50)),
        sa.Column('NameWindpark', sa.VARCHAR(50)),
        sa.Column('Lage', sa.VARCHAR(50)),
        sa.Column('Seelage', sa.VARCHAR(50)),
        sa.Column('ClusterOstsee', sa.VARCHAR(50)),
        sa.Column('ClusterNordsee', sa.VARCHAR(50)),
        sa.Column('Technologie', sa.VARCHAR(50)),
        sa.Column('Typenbezeichnung', sa.VARCHAR(50)),
        sa.Column('Nabenhoehe', sa.Float),
        sa.Column('Rotordurchmesser', sa.Float),
        sa.Column('Rotorblattenteisungssystem', sa.Float),
        sa.Column('AuflageAbschaltungLeistungsbegrenzung', sa.VARCHAR(50)),
        sa.Column('AuflagenAbschaltungSchallimmissionsschutzNachts', sa.VARCHAR(50)),
        sa.Column('AuflagenAbschaltungSchallimmissionsschutzTagsueber', sa.VARCHAR(50)),
        sa.Column('AuflagenAbschaltungSchattenwurf', sa.VARCHAR(50)),
        sa.Column('AuflagenAbschaltungTierschutz', sa.VARCHAR(50)),
        sa.Column('AuflagenAbschaltungEiswurf', sa.VARCHAR(50)),
        sa.Column('AuflagenAbschaltungSonstige', sa.VARCHAR(50)),
        sa.Column('Wassertiefe', sa.Float),
        sa.Column('Kuestenentfernung', sa.Float),
        sa.Column('EegMastrNummer_w', sa.VARCHAR(50)),
        sa.Column('HerstellerID', sa.VARCHAR(50)),
        sa.Column('HerstellerName', sa.VARCHAR(50)),
        sa.Column('version_w', sa.VARCHAR(50)),
        sa.Column('timestamp_w', sa.VARCHAR(50)),
        sa.Column('lid_e', sa.VARCHAR(50)),
        sa.Column('Ergebniscode_e', sa.VARCHAR(50)),
        sa.Column('AufrufVeraltet_e', sa.VARCHAR(50)),
        sa.Column('AufrufLebenszeitEnde_e', sa.VARCHAR(50)),
        sa.Column('AufrufVersion_e', sa.VARCHAR(50)),
        sa.Column('Meldedatum_e', sa.VARCHAR(50)),
        sa.Column('DatumLetzteAktualisierung_e', sa.VARCHAR(50)),
        sa.Column('EegInbetriebnahmedatum', sa.VARCHAR(50)),
        sa.Column('AnlagenkennzifferAnlagenregister', sa.VARCHAR(50)),
        sa.Column('AnlagenschluesselEeg', sa.VARCHAR(50)),
        sa.Column('PrototypAnlage', sa.VARCHAR(50)),
        sa.Column('PilotAnlage', sa.VARCHAR(50)),
        sa.Column('InstallierteLeistung', sa.Float),
        sa.Column('VerhaeltnisErtragsschaetzungReferenzertrag', sa.VARCHAR(50)),
        sa.Column('VerhaeltnisReferenzertragErtrag5Jahre', sa.VARCHAR(50)),
        sa.Column('VerhaeltnisReferenzertragErtrag10Jahre', sa.VARCHAR(50)),
        sa.Column('VerhaeltnisReferenzertragErtrag15Jahre', sa.VARCHAR(50)),
        sa.Column('AusschreibungZuschlag', sa.VARCHAR(50)),
        sa.Column('Zuschlagsnummer', sa.VARCHAR(50)),
        sa.Column('AnlageBetriebsstatus', sa.VARCHAR(50)),
        sa.Column('VerknuepfteEinheit', sa.VARCHAR(50)),
        sa.Column('version_e', sa.VARCHAR(50)),
        sa.Column('timestamp_e', sa.VARCHAR(50)),
        schema=schema_name
    )

    conn = engine.connect()
    print('Connection to OEP established')
    if not engine.dialect.has_table(conn, table_name_wind, schema_name):
        MastrWind.create()
        print(f'Created table {schema_name}.{table_name_wind}')
    else:
        print(f'Table {schema_name}.{table_name_wind} already exists')

    return conn, table_name_wind, schema_name


def read_wind(csv_name):
    """Read Wind from CSV file.

    Parameters
    ----------
    csv_name : str
        Name of file.

    Returns
    -------
    unit_wind : DataFrame
        Wind.
    """
    # log.info(f'Read data from {csv_name}')
    data_wind = pd.read_csv(csv_name, header=0, encoding='utf-8', sep=';', index_col=False,
                                dtype={'wind_id': int,
                                        'id': int,
                                        'lid': int,
                                        'EinheitMastrNummer': str,
                                        'Name': str,
                                        'Einheitart': str,
                                        'Einheittyp': str,
                                        'Standort': str,
                                        'Bruttoleistung': float,
                                        'Erzeugungsleistung': float,
                                        'EinheitBetriebsstatus': str,
                                        'Anlagenbetreiber': str,
                                        'EegMastrNummer': str,
                                        'KwkMastrNummer': str,
                                        'SpeMastrNummer': str,
                                        'GenMastrNummer': str,
                                        'BestandsanlageMastrNummer': str,
                                        'NichtVorhandenInMigriertenEinheiten': str,
                                        'StatisikFlag': str,
                                        'version': str,
                                        'timestamp': str,
                                        'lid_w': str,
                                        'Ergebniscode': str,
                                        'AufrufVeraltet': str,
                                        'AufrufLebenszeitEnde': str,
                                        'AufrufVersion': str,
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
                                        'Laengengrad': float,
                                        'Breitengrad': float,
                                        'UtmZonenwert': str,
                                        'UtmEast': float,
                                        'UtmNorth': float,
                                        'GaussKruegerHoch': float,
                                        'GaussKruegerRechts': float,
                                        'Meldedatum': str,
                                        'GeplantesInbetriebnahmedatum': str,
                                        'Inbetriebnahmedatum': str,
                                        'DatumEndgueltigeStilllegung': str,
                                        'DatumBeginnVoruebergehendeStilllegung': str,
                                        'DatumWiederaufnahmeBetrieb': str,
                                        'EinheitBetriebsstatus_w': str,
                                        'BestandsanlageMastrNummer_w': str,
                                        'NichtVorhandenInMigriertenEinheiten_w': str,
                                        'AltAnlagenbetreiberMastrNummer': str,
                                        'DatumDesBetreiberwechsels': str,
                                        'DatumRegistrierungDesBetreiberwechsels': str,
                                        'StatisikFlag_w': str,
                                        'NameStromerzeugungseinheit': str,
                                        'Weic': str,
                                        'WeicDisplayName': str,
                                        'Kraftwerksnummer': str,
                                        'Energietraeger': str,
                                        'Bruttoleistung_w': float,
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
                                        'GenMastrNummer_w': str,
                                        'NameWindpark': str,
                                        'Lage': str,
                                        'Seelage': str,
                                        'ClusterOstsee': str,
                                        'ClusterNordsee': str,
                                        'Technologie': str,
                                        'Typenbezeichnung': str,
                                        'Nabenhoehe': float,
                                        'Rotordurchmesser': float,
                                        'Rotorblattenteisungssystem': float,
                                        'AuflageAbschaltungLeistungsbegrenzung': str,
                                        'AuflagenAbschaltungSchallimmissionsschutzNachts': str,
                                        'AuflagenAbschaltungSchallimmissionsschutzTagsueber': str,
                                        'AuflagenAbschaltungSchattenwurf': str,
                                        'AuflagenAbschaltungTierschutz': str,
                                        'AuflagenAbschaltungEiswurf': str,
                                        'AuflagenAbschaltungSonstige': str,
                                        'Wassertiefe': float,
                                        'Kuestenentfernung': float,
                                        'EegMastrNummer_w': str,
                                        'HerstellerID': str,
                                        'HerstellerName': str,
                                        'version_w': str,
                                        'timestamp_w': str,
                                        'lid_e': str,
                                        'Ergebniscode_e': str,
                                        'AufrufVeraltet_e': str,
                                        'AufrufLebenszeitEnde_e': str,
                                        'AufrufVersion_e': str,
                                        'Meldedatum_e': str,
                                        'DatumLetzteAktualisierung_e': str,
                                        'EegInbetriebnahmedatum': str,
                                        'AnlagenkennzifferAnlagenregister': str,
                                        'AnlagenschluesselEeg': str,
                                        'PrototypAnlage': str,
                                        'PilotAnlage': str,
                                        'InstallierteLeistung': float,
                                        'VerhaeltnisErtragsschaetzungReferenzertrag': str,
                                        'VerhaeltnisReferenzertragErtrag5Jahre': str,
                                        'VerhaeltnisReferenzertragErtrag10Jahre': str,
                                        'VerhaeltnisReferenzertragErtrag15Jahre': str,
                                        'AusschreibungZuschlag': str,
                                        'Zuschlagsnummer': str,
                                        'AnlageBetriebsstatus': str,
                                        'VerknuepfteEinheit': str,
                                        'version_e': str,
                                        'timestamp_e': str})
    # log.info(f'Finished reading data from {csv_name}')
    return data_wind


def oep_upload_mastr_wind():
    """Create table for MaStR Wind

    """
    data_version = get_data_version()
    csv_wind = f'data/bnetza_mastr_{data_version}_wind.csv'
    data_wind = read_wind(csv_wind)
    #print(data_wind.head())

    conn, table_name_wind, schema_name = oep_create_mastr_wind()

    try:
        data_wind.to_sql(table_name_wind, conn, schema_name, if_exists='replace')
        print('Inserted data to ' + table_name_wind)
    except Exception as e:
        #session.rollback()
        raise
        print('Insert incomplete!')

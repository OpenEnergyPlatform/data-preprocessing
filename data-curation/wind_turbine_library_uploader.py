__copyright__ = "Reiner Lemoine Institut"
__license__   = "GNU General Public License Version 3 (GPLv3)"
__author__    = "christian-rli"

import os
import sys
import pandas as pd
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import ARRAY, TEXT, BIGINT, FLOAT, BOOLEAN
import oedialect

#os.environ['OEDIALECT_VERIFY_CERTIFICATE'] = 'FALSE'

if len(sys.argv) <= 1:
    print(
        "\n\tUpload data for the wind_turbine_library to the OEP with this script.\n"
        "\tYour data will be uploaded to a contribution table and later moved to the library.\n\n"

        "\tUsage: python wind_turbine_library_uploader.py [csv-FILE]\n\n"

        "\tYou will need username and token for the OEP to upload data. You may paste\n"
        "\tthem into this script, or you will be prompted every time you run it.\n"
    )
    sys.exit(0)


# Enter your OEP credentials below, so you don't have to enter them in the command line
# every time. White spaces in the username are fine!
#user = 'christian hofmann'
#token = 'b3a32baefe7d76a95f2eeddf41601fce665030b1'

user = 'christian hofmann'
token = 'b3a32baefe7d76a95f2eeddf41601fce665030b1'

if user == '':
    print("Enter your OEP username: ")
    user = input()
if token == "":
    print("Enter your OEP token: ")
    token = input()

print("\n")

# Create Engine:
OEP_URL = 'oep.iks.cs.ovgu.de'
OED_STRING = f'postgresql+oedialect://{user}:{token}@{OEP_URL}'

engine = sa.create_engine(OED_STRING)
metadata = sa.MetaData(bind=engine)

table_name = 'wind_turbine_library_contributions'
schema_name = 'model_draft'

wind_powercurves_df = pd.read_csv('turbine_library.csv', encoding='utf8', sep=',')

# define table
ContributionTable = sa.Table(
    table_name,
    metadata,
    sa.Column('id', BIGINT, primary_key=True),
    sa.Column('turbine_id', BIGINT),
    sa.Column('manufacturer', TEXT),
    sa.Column('name', TEXT),
    sa.Column('turbine_type', TEXT),
    sa.Column('nominal_power', FLOAT),
    sa.Column('rotor_diameter', FLOAT),
    sa.Column('rotor_area', FLOAT),
    sa.Column('hub_height', TEXT),
    sa.Column('max_speed_drive', FLOAT),
    sa.Column('wind_class_iec', TEXT),
    sa.Column('wind_zone_dibt', TEXT),
    sa.Column('power_density', FLOAT),
    sa.Column('power_density_2', FLOAT),
    sa.Column('calculated', BOOLEAN),
    sa.Column('has_power_curve', BOOLEAN),
    sa.Column('power_curve_wind_speeds', ARRAY(FLOAT)),
    sa.Column('power_curve_values', ARRAY(FLOAT)),
    sa.Column('has_cp_curve', BOOLEAN),
    sa.Column('power_coefficient_curve_wind_speeds', ARRAY(FLOAT)),
    sa.Column('power_coefficient_curve_values', ARRAY(FLOAT)),
    sa.Column('has_ct_curve', BOOLEAN),
    sa.Column('thrust_coefficient_curve_wind_speeds', ARRAY(FLOAT)),
    sa.Column('thrust_coefficient_curve_values', ARRAY(FLOAT)),
    sa.Column('source', TEXT),
    schema=schema_name,
)

# Create table if it doesn't exist
conn = engine.connect()
try:
    if not engine.dialect.has_table(conn, table_name, schema_name):
        ContributionTable.create()
except:
    raise
    print("Oops. Something didn't go as planned. Are you sure your credentials are working?")
finally:
    conn.close()

# write data to database
conn = engine.connect()
try: 
    print("writing to database...")
    wind_powercurves_df.to_sql(
        table_name, 
        conn, 
        schema_name, 
        if_exists='append',
    )
    print('Inserted data from ' + sys.argv[1] + ' to ' + table_name + ' :)')
except:
    print('Insert incomplete! :(')
    print("Are you sure your credentials are working and your data have the right format?")
    raise
finally:
    conn.close()
    print('Connection closed')

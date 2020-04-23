__copyright__ = "Reiner Lemoine Institut"
__license__   = "GNU Affero General Public License Version 3 (AGPL-3.0)"
__url__       = "https://github.com/openego/data_processing/blob/master/LICENSE"
__author__    = "Ludee"

import pandas as pd
import getpass
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
import oedialect
import geopandas as gpd

gdf_awz = pgd.read_file("bsh_seegrenzen_awz.gpkg")

print(gdf_awz)
__copyright__ = "Reiner Lemoine Institut"
__license__   = "GNU Affero General Public License Version 3 (AGPL-3.0)"
__url__       = "https://github.com/openego/data_processing/blob/master/LICENSE"
__author__    = "henhuy"

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as psql
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION


class DatabaseTypes:
    types = {
        "bigint": sa.BIGINT,
        "int": sa.INTEGER,
        "integer": sa.INTEGER,
        # not support with oedialect
        "double precision": DOUBLE_PRECISION,
        "double precision array": sa.ARRAY("DOUBLE_PRECISION"),
        "varchar": sa.VARCHAR,
        "json": sa.JSON,
        "text": sa.TEXT,
        "geometry point": Geometry("POINT"),
        "timestamp": sa.TIMESTAMP,
        "interval": sa.Interval,
        "string": sa.String,
        "float": sa.FLOAT,
        "boolean": sa.Boolean,
        "date": sa.Date,
        "geom": Geometry("GEOMETRY"),
        "geometry": Geometry("GEOMETRY")
    }

    def __getitem__(self, item):
        if item.split(" ")[-1] == "array":
            db_type = self.types[item[:-6]]
            return psql.ARRAY(db_type)
        else:
            return self.types[item]


TYPES = DatabaseTypes()

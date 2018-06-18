
import unittest
import db_io


class TestConnection(unittest.TestCase):
    def test_connection(self):
        """Connects to database and checks if schema "orig_vg250" exists"""

        db_io.CONFIG_FILENAME = '../db_io_config.ini'
        conn = db_io.db_session()
        result = conn.execute(
            "SELECT "
            "COUNT(*) AS schema_exists "
            "FROM information_schema.schemata "
            "WHERE schema_name = 'orig_vg250'"
        )
        self.assertEqual(next(result), (1, ))

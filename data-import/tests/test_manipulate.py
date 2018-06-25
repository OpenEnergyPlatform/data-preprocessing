
import unittest
import db_manipulate


class TestManipulation(unittest.TestCase):
    def test_manipulation(self):
        db_manipulate.download_folder = '../eGoPP'
        loader = db_manipulate.BaseDataLoader()
        files = loader.load_file()
        loader.get_shp_values(files)

import hashlib
import logging
import os
import unittest

from pathlib import Path

logging.basicConfig(level=logging.INFO)


class TestBaseClass(unittest.TestCase):
    def setUp(self):
        self.current_path = Path(os.path.dirname(os.path.realpath(__file__)))
        self.resource_folder = (self.current_path / "resources").absolute()
        self.temp_folder = (self.current_path / "temp").absolute()

    def tearDown(self):
        try:
            files = [f for f in os.listdir(self.temp_folder) if f.endswith(".txt")]
            logging.info("Cleaning up files {files}".format(files=files))
            for f in files:
                os.remove(os.path.join(self.temp_folder, f))
            logging.info("Completed cleanup")
        except OSError as e:
            raise e

    @staticmethod
    def compare_files(f1, f2):
        logging.info("Comparing {} and {}".format(f1, f2))
        file1, file2 = None, None

        try:
            file1 = open(file=f1, mode="r")
            file2 = open(file=f2, mode="r")

            hash1 = hashlib.sha1(file1.read().encode()).hexdigest()
            hash2 = hashlib.sha1(file2.read().encode()).hexdigest()

            return hash1 == hash2
        except FileNotFoundError as e:
            logging.error(e)
            raise e
        finally:
            if file1:
                file1.close()

            if file2:
                file2.close()

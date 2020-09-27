import logging
import unittest

from pyspark.sql.utils import AnalysisException

from data_processor import DataProcessor
from test.base_test import TestBaseClass

logging.basicConfig(level=logging.INFO)


class TestDataProcessor(TestBaseClass):
    def setUp(self):
        super(TestDataProcessor, self).setUp()
        spec_file = (self.resource_folder / "valid_data_processing_spec.json").absolute()
        self.data_processor = DataProcessor(spec_file=spec_file)

        self.existing_csv_file = (self.resource_folder / "output.csv").absolute()
        self.existing_hash_csv_file = (self.resource_folder / "output_hash.csv").absolute()

        self.csv_file = (self.temp_folder / "output.csv").absolute()
        self.hash_csv_file = (self.temp_folder / "output_hash.csv").absolute()

    def test_invalid_spec(self):
        with self.assertRaises(FileNotFoundError):
            DataProcessor(spec_file="nosuchfileexist.json")

        with self.assertRaises(ValueError):
            spec_file = (self.resource_folder / "invalid_data_processing_spec.json").absolute()
            self.data_processor = DataProcessor(spec_file=spec_file)

        with self.assertRaises(KeyError):
            spec_file = (self.resource_folder / "empty_data_processing_spec.json").absolute()
            self.invalid_data_processor = DataProcessor(spec_file=spec_file)

        with self.assertRaises(AnalysisException):
            self.data_processor.hash_csv_file(csv_file="filedoesnotexist.csv", hash_file=self.hash_csv_file)


    # def test_file_generation(self):
    #     self.data_processor.generate_csv_file(csv_file=self.csv_file, lines_count=10)
    #     self.data_processor.hash_csv_file(csv_file=str(self.csv_file), hash_file=str(self.hash_csv_file))

    def test_file_content(self):
        self.data_processor.hash_csv_file(csv_file=str(self.existing_csv_file), hash_file=str(self.hash_csv_file))
        #self.assertTrue(self.compare_files(self.hash_csv_file, self.existing_hash_csv_file))


if __name__ == '__main__':
    unittest.main()

import logging
import unittest

from file_parser import FileParser
from test.base_test import TestBaseClass

logging.basicConfig(level=logging.INFO)


class TestFileParser(TestBaseClass):
    def setUp(self):
        super(TestFileParser, self).setUp()

        spec_file = (self.resource_folder / "invalid_encoding_spec.json").absolute()
        self.invalid_encoding_parser = FileParser(spec_file=spec_file)

        spec_file = (self.resource_folder / "no_encoding_spec.json").absolute()
        self.no_encoding_parser = FileParser(spec_file=spec_file)

        spec_file = (self.resource_folder / "no_header_spec.json").absolute()
        self.no_header_parser = FileParser(spec_file=spec_file)

        spec_file = (self.resource_folder / "spec.json").absolute()
        self.valid_parser = FileParser(spec_file=spec_file)


        self.existing_fixed_width_file = (self.resource_folder / "fixed_width_file.txt").absolute()
        self.existing_delimited_file = (self.resource_folder / "delimited_file.txt").absolute()
        self.existing_delimited_file_with_header = (self.resource_folder / "delimited_file_with_header.txt").absolute()
        self.fixed_width_file = (self.temp_folder / "fixed_width_file.txt").absolute()
        self.delimited_file = (self.temp_folder / "delimited_file.txt").absolute()
        self.invalid_file = (self.temp_folder / "filedoesnotexist.txt").absolute()
        self.output_with_header_file = (self.temp_folder / "output_with_header.txt").absolute()
        self.output_without_header_file = (self.temp_folder / "output_without_header.txt").absolute()

    def test_invalid_spec(self):
        with self.assertRaises(FileNotFoundError):
            FileParser(spec_file=self.invalid_file)

    def test_generate_fixed_width_file_invalid_encoding(self):
        with self.assertRaises(LookupError):
            self.invalid_encoding_parser.generate_fixed_width_file(lines_count=10,
                                                                   fixed_width_file=self.fixed_width_file)

    def test_generate_delimited_file_invalid_input_file(self):
        with self.assertRaises(FileNotFoundError):
            self.invalid_encoding_parser.generate_delimited_file(fixed_width_file=self.invalid_file,
                                                                 delimited_file=self.delimited_file)

    def test_generate_delimited_file_invalid_encoding(self):
        self.valid_parser.generate_fixed_width_file(fixed_width_file=self.fixed_width_file, lines_count=10)

        with self.assertRaises(LookupError):
            self.invalid_encoding_parser.generate_delimited_file(fixed_width_file=self.fixed_width_file)

    def test_generate_fixed_width_file_invalid_columns(self):
        with self.assertRaises(ValueError):
            FileParser(spec_file="{folder}/invalid_columns_spec.json".format(folder=self.resource_folder))

    def test_generate_fixed_width_file_no_encoding(self):
        with self.assertRaises(KeyError):
            self.no_encoding_parser.generate_fixed_width_file(lines_count=10, fixed_width_file=self.fixed_width_file)

        self.valid_parser.generate_fixed_width_file(fixed_width_file=self.fixed_width_file, lines_count=10)

        with self.assertRaises(KeyError):
            self.no_encoding_parser.generate_delimited_file(fixed_width_file=self.fixed_width_file)

    def test_valid_spec(self):
        self.valid_parser.generate_fixed_width_file(fixed_width_file=self.fixed_width_file, lines_count=10)
        self.valid_parser.generate_delimited_file(
            fixed_width_file=self.fixed_width_file, delimited_file=self.delimited_file)
        self.no_header_parser.generate_delimited_file(
            fixed_width_file=self.fixed_width_file, delimited_file=self.delimited_file)

    def test_file_content_with_header(self):
        self.valid_parser.generate_delimited_file(
            fixed_width_file=self.existing_fixed_width_file, delimited_file=self.output_with_header_file)
        self.assertTrue(self.compare_files(self.existing_delimited_file_with_header, self.output_with_header_file))

    def test_file_content_without_header(self):
        self.no_header_parser.generate_delimited_file(
            fixed_width_file=self.existing_fixed_width_file, delimited_file=self.output_without_header_file)
        self.assertTrue(self.compare_files(self.existing_delimited_file, self.output_without_header_file))


if __name__ == '__main__':
    unittest.main()

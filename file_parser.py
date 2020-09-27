import csv
import json
import logging
import random
import string

logging.basicConfig(level=logging.INFO)


class FileParser:

    def __init__(self, spec_file):
        logging.info("Loading spec file {file}".format(file=spec_file))
        with open(spec_file) as f:
            self.spec = json.load(f)
            if len(self.spec["ColumnNames"]) != len(self.spec["Offsets"]):
                raise ValueError("Number of columns and offsets does not match")
            logging.info("Successfully loaded spec file {file}".format(file=spec_file))

    def generate_fixed_width_file(self, fixed_width_file="fixed_width_file.txt", delimiter=",", lines_count=None):
        output = None

        try:
            logging.info("Generating fixed width file {file}".format(file=fixed_width_file))
            output = open(file=fixed_width_file, mode="w+", encoding=self.spec["FixedWidthEncoding"])
            output_writer = csv.writer(output, delimiter=delimiter)
            headers = []
            for column, offset in zip(self.spec["ColumnNames"], self.spec["Offsets"]):
                headers.append("{column}{spaces}".format(column=column, spaces=" " * (int(offset) - len(column))))

            output_writer.writerow(headers)

            # Generating random data lines
            for i in range(lines_count):
                row = []
                for offset in self.spec["Offsets"]:
                    random_value = random.choices(string.ascii_uppercase + string.digits,
                                                  k=random.randrange(int(offset)))
                    row.append("{random_value}{spaces}".format(random_value="".join(random_value),
                                                                spaces=" " * (int(offset) - len(random_value))))
                output_writer.writerow(row)

            logging.info("Generated fixed width file {file}".format(file=fixed_width_file))
        except Exception as e:
            logging.error(e, "Failed to generate fixed width file {file}".format(file=fixed_width_file))
            raise e
        finally:
            if output:
                output.close()

    def generate_delimited_file(self, fixed_width_file, input_delimiter=",", delimited_file="delimited_file.txt",
                                output_delimiter=","):
        _input, output = None, None

        try:
            logging.info("Generating delimited file {file}".format(file=delimited_file))

            _input = open(file=fixed_width_file, mode="r", encoding=self.spec["FixedWidthEncoding"])
            input_reader = csv.reader(_input, delimiter=input_delimiter)

            output = open(file=delimited_file, mode="w+", encoding=self.spec["DelimitedEncoding"])
            output_writer = csv.writer(output, delimiter=output_delimiter)

            for idx, row in enumerate(input_reader):
                if idx == 0 and not self.spec["IncludeHeader"] == "True":
                    continue

                strip_row = []
                for column in row:
                    strip_row.append(column.strip())
                output_writer.writerow(strip_row)

            logging.info("Generated delimited file {file}".format(file=delimited_file))
        except FileNotFoundError as e:
            logging.error(e, "Failed to generate delimited file {file}".format(file=delimited_file))
            raise e
        finally:
            if output:
                output.close()

            if _input:
                _input.close()

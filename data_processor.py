import csv
import hashlib
import json
import logging
import random
import string

from pyspark.shell import spark
from pyspark.sql.functions import when, udf
from pyspark.sql.types import StringType

logging.basicConfig(level=logging.INFO)


class DataProcessor:

    def __init__(self, spec_file):
        logging.info("Loading spec file {file}".format(file=spec_file))
        with open(spec_file) as f:
            self.spec = json.load(f)
            if len(self.spec["ColumnNames"]) != len(self.spec["anonymise"]):
                raise ValueError("Number of columns and anonymise does not match")
            logging.info("Successfully loaded spec file {file}".format(file=spec_file))

    def generate_csv_file(self, csv_file="data.csv", lines_count=None, column_value_length=10):
        output = None

        try:
            logging.info("Generating csv file {file}".format(file=csv_file))
            output = open(file=csv_file, mode="w+")
            output_writer = csv.writer(output, delimiter=",")
            output_writer.writerow(self.spec["ColumnNames"])

            # Generating random data lines
            columns = len(self.spec["ColumnNames"])
            for i in range(lines_count):
                row = []
                for _ in range(columns):
                    random_value = random.choices(string.ascii_uppercase + string.digits,
                                                  k=random.randrange(column_value_length))
                    row.append("".join(random_value))
                output_writer.writerow(row)

            logging.info("Generated csv file {file}".format(file=csv_file))
        finally:
            if output:
                output.close()

    def hash_csv_file(self, csv_file="data.csv", hash_file="hash_data.csv"):
        _input, output = None, None

        try:
            logging.info("Generating hashed csv file {file}".format(file=hash_file))


            df = spark.read.csv(csv_file, header='true')
            columns = df.schema.names
            for column, anonymise in zip(columns, self.spec["anonymise"]):
                encode = udf(lambda x: hashlib.sha1(x.encode()) if anonymise == "True" else x, StringType())
                df = df.withColumn(column, encode(df[column]))


            df.write.csv(hash_file, header='true', mode='overwrite')
            logging.info("Generated hashed csv file {file}".format(file=hash_file))
        except Exception as e:
            logging.error(e, "Failed to generate hashed csv file {file}".format(file=hash_file))
            raise e
        finally:
            if output:
                output.close()

            if _input:
                _input.close()

# dataprocessing


## Download docker image

docker pull bhasin85/dataprocessing:latest

## Go to docker terminal

docker run -it bhasin85/dataprocessing:latest bin/bash

## Help Command

python run.py --help

## Generate Fixed Width File

python run.py --type fp --spec_file resources/spec.json --generate_fix_width_file fixed_width_file.txt

## Generate Delimited File using Fixed Width File

python run.py --type fp --spec_file resources/spec.json --generate_delimited_file delimited_file.txt --fix_width_file fixed_width_file.txt 

## Generate CSV File

python run.py --type dp --spec_file resources/data_processing_spec.json --generate_csv_file data.csv

## Generate Hashed CSV File

python run.py --type dp --spec_file resources/data_processing_spec.json --hash_csv_file hash_data.csv --csv_file data.csv

## Run Unit Tests

python -m unittest discover -p '*_test.py'
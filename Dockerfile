FROM python:3

ADD resources /
ADD test /
ADD data_processor.py /
ADD file_parser.py /

RUN pip install pyspark

CMD [ "python", "./my_script.py" ]
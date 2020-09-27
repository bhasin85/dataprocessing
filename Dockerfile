FROM openjdk:slim
COPY --from=python:3.6 / /
RUN pip install pyspark
RUN pip install pandas
RUN pip install findspark
COPY . /
CMD [ "python", "./run.py" ]
#CMD ["python", "-m", "unittest", "discover", "-p", "*_test.py"]
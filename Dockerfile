FROM python:3.6-stretch
RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y
RUN apt-get install -y python3-dev
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade cython
RUN pip3 install setuptools_scm
ADD ./requirements.txt ./
COPY edit_housing.py ./
COPY edit_housing_technic.py ./
COPY test_pandas_profiler.py ./
COPY housing_report_data_test.py ./
COPY great_expectations /great_expectations
RUN pip3 install  -r requirements.txt
ENTRYPOINT ["/usr/local/bin/python", "-m", "awslambdaric"]
CMD ["housing_report_data_test.handler"]

FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN export AIRFLOW_HOME=$(pwd)
RUN airflow initdb
RUN python remove_airflow_examples.py
RUN airflow resetdb -y
RUN python customize_dashboard.py

CMD airflow webserver -p=$PORT

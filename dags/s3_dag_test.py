"""
S3 Sensor Connection Test

NOTE FOR THIS TO WORK YOU MUST SET UP AN S3 CONNECTION PER THESE INSTRUCTIONS:
https://stackoverflow.com/questions/39997714/airflow-s3-connection-using-ui/40774361#40774361

"""

from airflow import DAG
from airflow.operators import SimpleHttpOperator, HttpSensor, EmailOperator
from airflow.operators import BashOperator
from airflow.operators import S3KeySensor
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2017, 12, 1),
    'email': ['test@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 20,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG('s3_dag_test', default_args=default_args, schedule_interval= '@once')

t1 = BashOperator(
    task_id='bash_test',
    bash_command='echo "hello, it should work" > s3_conn_test.txt',
    dag=dag)

sensor = S3KeySensor(
    task_id='check_s3_for_file_in_s3',
    bucket_key='file-to-watch-*',
    wildcard_match=True,
    bucket_name='airflow-bucket',
    s3_conn_id='my_conn_S3',
    timeout=18*60*60,
    poke_interval=120,
    dag=dag)

t1.set_upstream(sensor)
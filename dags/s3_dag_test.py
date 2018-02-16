"""
S3 Sensor Connection Test

NOTE FOR THIS TO WORK YOU MUST SET UP AN S3 CONNECTION PER THESE INSTRUCTIONS:
https://stackoverflow.com/questions/39997714/airflow-s3-connection-using-ui/40774361#40774361

"""

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.sensors import S3KeySensor
from datetime import datetime, timedelta
from airflow.hooks.S3_hook import S3Hook
import boto

default_args = {
    'owner': 'brighthive',
    'depends_on_past': False,
    'start_date': datetime(2018, 2, 15),
    'email': ['enginnering@brighthive.io'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 20,
    'retry_delay': timedelta(minutes=1)
}


def grab_file():
    s3_conn_id = 'my_conn_S3'
    s3 = S3Hook(s3_conn_id)

    key_label = "file-to-watch*.txt"
    key = s3.get_key(key_label, 'int1-source')
    key_string = key.get_contents_as_string()

    return key_string


dag = DAG('s3_connect_dag', default_args=default_args, schedule_interval='@once')

file_processor = PythonOperator(
    task_id='grab_file_from_s3',
    python_callable=grab_file,
    dag=dag)

file_trigger = S3KeySensor(
    task_id='check_s3_for_file_in_s3',
    bucket_key='file-to-watch-*',
    wildcard_match=True,
    bucket_name='int1-source',
    s3_conn_id='my_conn_S3',
    timeout=18*60*60,
    poke_interval=120,
    dag=dag)

file_processor.set_upstream(file_trigger)

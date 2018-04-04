import logging
import datetime as dt
from urllib.parse import urlparse
import os
import boto3
from tempfile import NamedTemporaryFile
import psycopg2

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.sensors import S3KeySensor
from airflow.hooks import postgres_hook, S3_hook
from airflow.utils.decorators import apply_defaults
from airflow.exceptions import AirflowException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Brighthive Engineering team')

AGRS = ['integration-source', '1valid.csv']


def s3_connect(self, parameter_list):
    hook = S3_hook.S3Hook(aws_conn_id=self.aws_conn_id)
    hook.check_for_key(self.bucket_key, self.bucket_name)


def grab_file(bucket, key):
    # Use Variable.get('aws_access_key_id') in future
    client = boto3.client(
        's3',
        aws_access_key_id='',
        aws_secret_access_key=''
    )
    client.download_file(bucket, key, '/tmp/{}'.format(key))
    logger.info('Downloaded file {} locally'.format(key))
    return '/tmp/{}'.format(key)


def commit_to_db():
    DB = ''
    result = urlparse(DB)

    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname

    logger.info('Connecting to database {}'.format(DB))
    connection = psycopg2.connect(
        database=database,
        user=username,
        password=password,
        host=hostname
    )

    logger.info('Database connected')
    logger.debug('Database {} is on host {}'.format(database, hostname))
    cur = connection.cursor()

    # the 'organization' below can be replaced by any table in the db
    with open(grab_file(OP_AGRS[0], OP_AGRS[1]), 'r') as f:
        cur.copy_from(f, 'organization', sep=',')

    connection.commit()


default_args = {
    'owner': 'matt@brighthive.io',
    'start_date': dt.datetime(2017, 3, 10),
    'retries': 5,
    'retry_delay': dt.timedelta(minutes=1),
}


with DAG('programs_registry_db',
         default_args=default_args,
         schedule_interval='@once',
         ) as dag:

    commit_to_db = PythonOperator(task_id='commit_to_db',
                                  python_callable=commit_to_db)

    grab_file = PythonOperator(task_id='grab_file',
                               python_callable=grab_file,
                               op_args=AGRS)

    source_file_trigger = S3KeySensor(task_id='check_for_file_in_source_s3',
                                      bucket_key=AGRS[1],
                                      bucket_name=AGRS[0],
                                      aws_conn_id='integration',
                                      timeout=18*60*60,
                                      poke_interval=10)


grab_file.set_upstream(source_file_trigger)
commit_to_db.set_upstream(grab_file)

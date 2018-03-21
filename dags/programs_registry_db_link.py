import datetime as dt
from urllib.parse import urlparse
import psycopg2
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.sensors import S3KeySensor
from airflow.hooks import postgres_hook, S3_hook


def grab_file():
    aws_conn_id = 'integration'
    s3 = S3_hook.S3Hook(aws_conn_id)

    key_label = "*.csv"
    key = s3.get_key(key_label, 'integration-target')
    key_string = key.get_contents_as_string()

    return key_string


def commit_to_db():
    pg_hook = postgres_hook.PostgresHook(postgres_conn_id='registry')
    # pg_hook.run(SQL) but not for this case ...

    result = urlparse(pg_hook)

    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname

    connection = psycopg2.connect(
        database=database,
        user=username,
        password=password,
        host=hostname
    )

    cur = connection.cursor()
    cur.copy_from(f, 'organization', sep=',')

    connection.commit()


default_args = {
    'owner': 'stanley@brighthive.io',
    'start_date': dt.datetime(2017, 3, 10),
    'retries': 5,
    'retry_delay': dt.timedelta(minutes=1),
}

with DAG('programs_registry_db',
         default_args=default_args,
         schedule_interval='@once',
         ) as dag:

    s3_connect = BashOperator(task_id='s3_connect',
                              bash_command='echo "Listening for s3 bucket upload"')

    commit_to_db = PythonOperator(task_id='commit_to_db',
                                  python_callable=commit_to_db)

target_file_trigger = S3KeySensor(
    task_id='check_for_file_in_target_s3',
    bucket_key='*',
    wildcard_match=True,
    bucket_name='integration-target',
    aws_conn_id='integration',
    timeout=18*60*60,
    poke_interval=10,
    dag=dag)


target_file_trigger.set_upstream(s3_connect)
commit_to_db.set_upstream(target_file_trigger)

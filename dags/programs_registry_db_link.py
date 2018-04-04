import logging
import datetime as dt
from urllib.parse import urlparse
import os

import psycopg2
from airflow import DAG
from airflow.operators.s3_file_transform_operator import S3FileTransformOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.sensors import S3KeySensor
from airflow.hooks import postgres_hook, S3_hook
from airflow.utils.decorators import apply_defaults
from airflow.exceptions import AirflowException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Brighthive Engineering team')


class S3FileRenameOperator(S3FileTransformOperator):
    """
    Borrows from S3FileTransformOperator class

    :param source_s3_key: The key to be retrieved from S3
    :type source_s3_key: str
    :param source_s3_bucket: source s3 bucket
    :type source_s3_bucket: str
    :param source_aws_conn_id: source s3 connection
    :type source_aws_conn_id: str
    :param dest_s3_key: The key to be written from S3
    :type dest_s3_key: str
    :param dest_s3_bucket: destination s3 bucket
    :type dest_s3_bucket: str
    :param dest_aws_conn_id: destination s3 connection
    :type dest_aws_conn_id: str
    :param replace: Replace dest S3 key if it already exists
    :type replace: bool
    :param transform_script: location of the executable transformation script
    :type transform_script: str
    """

    template_fields = ('source_s3_key', 'dest_s3_key')
    template_ext = ()
    ui_color = '#f9c915'

    @apply_defaults
    def __init__(
            self,
            source_s3_key,
            dest_s3_key,
            source_s3_bucket,
            dest_s3_bucket,
            transform_script,
            source_aws_conn_id='aws_default',
            dest_aws_conn_id='aws_default',
            replace=False,
            *args, **kwargs):
        super(S3FileRenameOperator, self).__init__(source_s3_key=source_s3_key, dest_s3_key=dest_s3_key, transform_script=transform_script, *args, **kwargs)
        self.source_s3_key = source_s3_key
        self.source_s3_bucket = source_s3_bucket
        self.source_aws_conn_id = source_aws_conn_id
        self.dest_s3_key = dest_s3_key
        self.dest_s3_bucket = dest_s3_bucket
        self.dest_aws_conn_id = dest_aws_conn_id
        self.replace = replace
        self.transform_script = transform_script

    def execute(self, context):
        source_s3 = S3_hook.S3Hook(aws_conn_id=self.source_aws_conn_id)
        dest_s3 = S3_hook.S3Hook(aws_conn_id=self.dest_aws_conn_id)
        self.log.info("Downloading source S3 file %s", self.source_s3_key)
        if not source_s3.check_for_key(self.source_s3_key, bucket_name=None):
            raise AirflowException(
                "The source key {0} in {1} does not exist".format(
                    self.source_s3_key, self.source_s3_bucket))
        source_s3_key_object = source_s3.get_key(
            self.source_s3_key, bucket_name=self.source_s3_bucket)
        with NamedTemporaryFile("w") as f_source, NamedTemporaryFile("w") as f_dest:
            self.log.info(
                "Dumping S3 file %s contents to local file %s",
                self.source_s3_key, f_source.name
            )
            source_s3_key_object.get_contents_to_file(f_source)
            f_source.flush()
            source_s3.connection.close()
            transform_script_process = subprocess.Popen(
                [self.transform_script, f_source.name, f_dest.name],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (transform_script_stdoutdata,
             transform_script_stderrdata) = transform_script_process.communicate()
            self.log.info("Transform script stdout %s",
                          transform_script_stdoutdata)
            if transform_script_process.returncode > 0:
                raise AirflowException(
                    "Transform script failed %s", transform_script_stderrdata)
            else:
                self.log.info(
                    "Transform script successful. Output temporarily located at %s",
                    f_dest.name
                )
            self.log.info("Uploading transformed file to S3")
            f_dest.flush()
            dest_s3.load_file(
                filename=f_dest.name,
                key=self.dest_s3_key,
                bucket_name=self.dest_s3_bucket,
                replace=self.replace
            )
            self.log.info("Upload successful")
            dest_s3.connection.close()


def commit_to_db():
    # I'll revisit this later

    # pg_hook = postgres_hook.PostgresHook(postgres_conn_id='registry')
    # pg_hook.run()
    DB = os.getenv('DATABASE_URL')
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
    cur.copy_from(grab_file(), 'organization', sep=',')

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

    s3_connect = BashOperator(task_id='s3_connect',
                              bash_command='echo \
                              "Listening for file upload to s3"')

    grab_file = S3FileRenameOperator(task_id='grab_file',
                                     source_s3_key='1valid.csv',
                                     dest_s3_key='vvvalid.csv',
                                     source_s3_bucket='int-source',
                                     dest_s3_bucket='int-source',
                                     transform_script='mv',
                                     source_aws_conn_id='integration',
                                     dest_aws_conn_id='integration',
                                     )

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
grab_file.set_upstream(target_file_trigger)
commit_to_db.set_upstream(grab_file)

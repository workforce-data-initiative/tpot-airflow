from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'Stan_MD',
    'depends_on_the_past': False,
    'start_date': datetime(2017, 8, 1),
    'email': 'stanley@brighthive.io',
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    # Changing this to seconds for development purposes
    'retry_delay': timedelta(seconds=15)
}

dag = DAG('tpot', default_args=default_args)

# A task must have owner and task_id arguments
task_one = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag)

task_two = BashOperator(
    task_id='sleep',
    bash_command='sleep 5',
    retries=3,
    dag=dag)

templated_command = """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
        echo "{{ params.my_param }}"
    {% endfor %}
"""

task_three = BashOperator(
    task_id='templated',
    bash_command=templated_command,
    params={'my_param': "Parameter I passed in"},
    dag=dag)

task_two.set_upstream(task_one)
task_three.set_upstream(task_one)

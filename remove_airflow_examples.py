import os
import sys
import fileinput

file = '/root/airflow/airflow.cfg'

for i, line in enumerate(fileinput.input(file, inplace=1)):
    sys.stdout.write(line.replace('load_examples = True',
                                  'load_examples = False'))

for i, line in enumerate(fileinput.input(file, inplace=1)):
    sys.stdout.write(line.replace('dags_folder = /root/airflow/dags',
                                  'dags_folder = /usr/src/app/dags'))

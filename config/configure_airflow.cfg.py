import os
import sys
import fileinput
import logging
from cryptography.fernet import Fernet

FERNET_KEY = Fernet.generate_key().decode()
file = os.getenv('AIRFLOW_HOME') + '/airflow.cfg'

for i, line in enumerate(fileinput.input(file, inplace=1)):
    sys.stdout.write(line.replace('load_examples = True',
                                  'load_examples = False'))
for i, line in enumerate(fileinput.input(file, inplace=1)):
    sys.stdout.write(line.replace('#AIRFLOW_HOME#',
                                  os.getenv('AIRFLOW_HOME')))
for i, line in enumerate(fileinput.input(file, inplace=1)):
    sys.stdout.write(line.replace('#FERNET_KEY#', FERNET_KEY))


logging.info("Removing Example DAGs")
logging.info("Setting AIRFLOW_HOME and FERNET_KEY in airflow.cfg")

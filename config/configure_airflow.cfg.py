import os
import sys
import fileinput
import logging
from cryptography.fernet import Fernet

FERNET_KEY = Fernet.generate_key().decode()
AIRFLOW_HOME = os.getenv('AIRFLOW_HOME')
file = AIRFLOW_HOME + '/airflow.cfg'

for i, line in enumerate(fileinput.input(file, inplace=1)):
    sys.stdout.write(line.replace('load_examples = True',
                                  'load_examples = False'))
for i, line in enumerate(fileinput.input(file, inplace=1)):
    sys.stdout.write(line.replace('#FERNET_KEY#', FERNET_KEY))

for i, line in enumerate(fileinput.input(file, inplace=1)):
    sys.stdout.write(line.replace('#AIRFLOW_HOME#', AIRFLOW_HOME))

for i, line in enumerate(fileinput.input(file, inplace=1)):
    sys.stdout.write(line.replace('#GOOGLE_CLIENT_ID#',
                                  os.getenv('GOOGLE_CLIENT_ID')))

for i, line in enumerate(fileinput.input(file, inplace=1)):
    sys.stdout.write(line.replace('#GOOGLE_CLIENT_SECRET#',
                                  os.getenv('GOOGLE_CLIENT_SECRET')))

logging.info("Removing Example DAGs")
logging.info("Setting AIRFLOW_HOME, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET and \
FERNET_KEY in airflow.cfg")

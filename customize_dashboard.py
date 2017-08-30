import sys
import fileinput

file = '/usr/local/lib/python3.6/site-packages/airflow/www/templates/admin/\
master.html'

for i, line in enumerate(fileinput.input(file, inplace=1)):
    sys.stdout.write(line.replace('<span>Airflow</span>',
                                  '<span>TPOT - Airflow</span>'))

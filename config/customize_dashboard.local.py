import os
import logging
import sys
import fileinput

file = os.getenv("VIRTUAL_ENV")+'/lib/python'+sys.version[:3]+'/site-packages/\
airflow/www/templates/admin/master.html'

for i, line in enumerate(fileinput.input(file, inplace=1)):
    sys.stdout.write(line.replace('<span>Airflow</span>',
                                  "<span>{} - Workflow Manager</span>".format(
                                      os.getenv('APP', 'TPOT'))))

logging.info("Setting APP as {}".format(os.getenv('APP', 'TPOT')))

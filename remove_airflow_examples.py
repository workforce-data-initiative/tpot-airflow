import os
import sys
import fileinput

file = 'airflow.cfg'

for i, line in enumerate(fileinput.input(file, inplace=1)):
    sys.stdout.write(line.replace('load_examples = True',
                                  'load_examples = False'))

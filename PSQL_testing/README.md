# CSV to PSQL

Ensure that the packages are installed. The command to do this is:

`pip install -r requirements.txt`

Next, having created a Postgres DB, run:

`export TEST_DATABASE_URL=postgresql://username:password@localhost:5432/db`

Finally run:

`python create_table.py && python csv_to_psql.py`

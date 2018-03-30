import logging
import os
from urllib.parse import urlparse

import psycopg2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

result = urlparse(os.getenv('TEST_DATABASE_URL'))
# In the format: "postgresql://postgres:postgres@localhost:5432/postgres"
# or: "postgresql://localhost:5432/postgres"
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname

logger.info('Connecting to database')
connection = psycopg2.connect(
    database=database,
    user=username,
    password=password,
    host=hostname
)
logger.info('Database connected')
logger.debug('Database {} is on host {}'.format(database, hostname))

cur = connection.cursor()
cur.execute("""
CREATE TABLE users(
    id integer PRIMARY KEY,
    _id text,
    name text,
    slug text
)
""")
connection.commit()
logger.info('Table created')

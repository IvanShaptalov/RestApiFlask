"""DATABASE URL PATTERN: <driver>://<username>:<password>@<host>/<dbname>,
LOCAL PATTERN <driver>://<path_to_db>"""
import os
from config.config import config

DB_PATH = "app/models/"

DATABASE_URL = os.environ.get('DATABASE_URL') or config['DATABASE']['URL']
DATABASE_TEST_URL = os.environ.get('DATABASE_TEST_URL') or config['DATABASE']['TEST_URL']

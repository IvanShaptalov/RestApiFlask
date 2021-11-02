import configparser
import os
from pathlib import Path

# paths

BASE_DIR = Path(__file__).resolve().parent.parent
print('config ')
APPLICATION_PATH = os.path.join(BASE_DIR, "app")
CONFIG_PATH = os.path.join(BASE_DIR, "config/config.ini")
MEDIA_PATH = os.path.join(BASE_DIR, "app/media/")
DB_PATH = "app/models/"

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

SECRET_KEY = os.environ.get('SECRET_KEY') or config['KEYS']['SECRET_KEY']

DB_DRIVER = os.environ.get('DB_DRIVER') or config['DATABASE']['DRIVER']
DB_NAME = os.environ.get('DATABASE_URL') or config['DATABASE']['URL']
DATABASE_URL = "{}{}{}".format(DB_DRIVER, DB_PATH, DB_NAME)

# database to testing
DB_TEST_NAME = os.environ.get('DATABASE_TEST_URL') or config['DATABASE']['TEST_URL']
DATABASE_TEST_URL = "{}{}".format(DB_DRIVER, DB_TEST_NAME)

# secure
JW_TOKEN_MINUTES_LIVE = int(os.environ.get('JW_TOKEN_MINUTES_LIVE') or config['JWT']['LIVE_MINUTES'])

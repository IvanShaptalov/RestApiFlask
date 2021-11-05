import configparser
import os
from pathlib import Path

# paths

BASE_DIR = Path(__file__).resolve().parent.parent
print('config ')
APPLICATION_PATH = os.path.join(BASE_DIR, "app")
CONFIG_PATH = os.path.join(BASE_DIR, "config/config.ini")
MEDIA_PATH = os.path.join(BASE_DIR, "app/media/")

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

SECRET_KEY = os.environ.get('SECRET_KEY') or config['KEYS']['SECRET_KEY']

# secure
JW_TOKEN_MINUTES_LIVE = int(os.environ.get('JW_TOKEN_MINUTES_LIVE') or config['JWT']['LIVE_MINUTES'])

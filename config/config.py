import configparser
import os
from pathlib import Path
# paths
BASE_DIR = Path(__file__).resolve().parent

CONFIG_PATH = os.path.join(BASE_DIR, "config/config.ini")
MEDIA_PATH = os.path.join(BASE_DIR, "app/media/")

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

DATABASE_URL = os.environ.get('DATABASE_URL') or ''


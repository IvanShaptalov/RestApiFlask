import pytest

# from filters.filters import user_in_chat
from config import config


@pytest.mark.config
def test_config_valid():
    assert config.BASE_DIR
    assert config.CONFIG_PATH
    assert config.MEDIA_PATH
    assert config.DB_PATH
    assert config.DB_DRIVER
    assert config.DB_NAME
    assert config.SECRET_KEY
    assert config.DATABASE_URL
    assert config.JW_TOKEN_MINUTES_LIVE


@pytest.mark.internet
def test_internet_connection():
    import requests
    google = 'https://www.google.com/'
    try:
        requests.get(google)
    except Exception as e:
        print(e)
        assert False, 'check internet connection'

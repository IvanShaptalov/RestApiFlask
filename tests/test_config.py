import pytest


@pytest.mark.config
def test_configuration():
    from config import config
    assert config.BASE_DIR is not None
    assert config.CONFIG_PATH is not None
    assert config.MEDIA_PATH is not None
    assert config.APPLICATION_PATH is not None
    assert config.SECRET_KEY is not None
    assert config.JW_TOKEN_MINUTES_LIVE is not None


@pytest.mark.config
def test_db_configuration():
    from config import db_config
    assert db_config.DB_PATH is not None
    assert db_config.DATABASE_URL != db_config.DATABASE_TEST_URL, "DATABASE_TEST_URL must have another path "


@pytest.mark.internet
def test_internet_connection():
    import requests
    google = 'https://www.google.com/'
    try:

        response = requests.get(google)
        assert response.status_code == 200, "check internet connection"
    except Exception as e:
        print(e)
        assert False, "check internet connection"

import logging
from base64 import b64encode

import pytest

import config.config
from app.api import create_app
from app.models import db_util


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    # create the app with common test config
    print('fixture working?')
    app = create_app(test_config={"TESTING": True, "DATABASE": config.config.DATABASE_TEST_URL})
    assert db_util.Base is not None
    assert db_util.engine is not None
    return app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def registration_data():
    return dict(name="ivan_test",
                password="testdskjf8243u209hf2")


def login_headers(missed_username=False, missed_password=False):
    username, password = "ivan_test", "testdskjf8243u209hf2"
    if missed_username:
        username = ""
    if missed_password:
        password = ""
    encoded_credentials = b64encode(bytes(f'{username}:{password}',
                                          encoding='ascii')).decode('ascii')
    return {'Authorization': f'Basic {encoded_credentials}'}


@pytest.fixture
def registration_data_1():
    return dict(name="test_name_2",
                password="testdsk32432jfu209hf2")


@pytest.fixture
def r_data_pass_missed():
    return dict(name="ivan_test")


@pytest.fixture
def r_data_pass_weak():
    pass_len_bigger_than_max = "password" * 1000
    return [dict(name="ivan_test_1", password="1234"),
            dict(name="ivan_test_2", password="halol"),
            dict(name="ivan_test_3", password="less"),
            dict(name="ivan_test_4", password="________errorr____"),
            dict(name="ivan_test_5", password="testjust symbols and space"),
            dict(name="ivan_test_6", password="&*#&$@)($*#(R*YFU)P*OEIHWJFP(*"),
            dict(name="ivan_test_6", password=pass_len_bigger_than_max)]


@pytest.fixture
def r_data_name_invalid():
    strong_pass = "Str32on234g@password"
    return [dict(name="iv", password=strong_pass),
            dict(name="i", password=strong_pass),
            dict(name="", password=strong_pass),
            dict(password=strong_pass),
            dict(name="i", password=strong_pass),
            dict(name=".", password=strong_pass)]


@pytest.fixture
def delete_aliases_caller():
    return _delete_aliases


def _delete_aliases():
    db_util.Base.metadata.drop_all(db_util.engine)
    logging.info('delete aliases')

import logging
from base64 import b64encode

import pytest

import config.config
from app.api import create_app
from app.models import db_util
from config import routes


@pytest.fixture
def app():
    """Create and configure a new app instance for each """
    # create a temporary file to isolate the database for each
    # create the app with common testing config
    print('fixture working?')
    app = create_app(test_config={"TESTING": True, "DATABASE": config.config.DATABASE_TEST_URL})
    assert db_util.Base is not None
    assert db_util.engine is not None
    return app


@pytest.fixture
def client(app):
    """A testing client for the app."""
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


@pytest.fixture
def number_list_invalid():
    return ['hfj',
            'fsgd23232',
            '32498gsdgfji',
            'sgjfJHOIFGS',
            '-132,,123']


@pytest.fixture
def number_list_valid():
    return ['1233',
            '213.123',
            '12498.123',
            '-123.1',
            '-0',
            '-1',
            '001'
            ]


@pytest.fixture
def number_list_above_zero():
    return [1, 2, 3, 4, 5, 6, 7, 8, 8, 9, 10]


@pytest.fixture
def number_list_below_zero():
    return [-1, -2, -3, -4 - 5, -6, -6 - 7, -9, -10000]


def _delete_aliases():
    db_util.Base.metadata.drop_all(db_util.engine)
    logging.info('delete aliases')


@pytest.fixture
def token(client, registration_data, delete_aliases_caller):
    login_response = None
    # noinspection PyBroadException
    try:
        # create user
        response = client.post(routes.AUTH_PREFIX + routes.REGISTER, json=registration_data)
        if len(response.headers) > 0:
            print(response.headers[0])
        assert response.status_code == 201, "expected 201, user creating"

        login_response = client.post(routes.AUTH_PREFIX + routes.LOGIN, headers=login_headers())
        print(response)
        assert login_response.status_code == 200, "login don't work correctly"
    except:
        delete_aliases_caller()
    finally:
        if login_response is not None:
            data = login_response.get_json()
            return data['token']


@pytest.fixture
def product_valid():
    return {"article": "3249uef123ho3weih32f23rijfjoes76789",
            "name": "apples"}


@pytest.fixture
def products_invalid():
    very_big_name = "apples" * 1000
    very_big_article = "article" * 1000
    return [{"article": "",
             "name": ""},
            {"name": "apples"},
            {"article": very_big_article,
             "name": very_big_name}]


@pytest.fixture
def valid_pricelist():
    return [{"currency": "usd", "count": 390},
            {"currency": "uah", "count": 2000},
            {"currency": "uah1", "count": "200"},
            {"currency": "uah2", "count": "20.10"},
            {"currency": "ru", "count": 20.1234}]


@pytest.fixture
def invalid_pricelist():
    return [{"currency": "usd", "count": -3 - 90},
            {"currency": "uah", "count": -2000},
            {"currency": "uah", "count": "hello"},
            {"currency": "uah", "count": "200, maybe ok?"},
            {"currency": "ru", "count": -20}]


@pytest.fixture
def pricelist_unique_failed():
    return [{"currency": "uah", "count": 2000},
            {"currency": "uah", "count": 20.1234}]


@pytest.fixture
def change_username():
    return {"name": "new_test_username"}


@pytest.fixture
def pagination_args():
    return "?page=4&page_size=1"
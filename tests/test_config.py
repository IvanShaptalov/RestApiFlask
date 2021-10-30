from unittest import TestCase

from config import config
from tests.conftest import BaseTestCase


class ConfigTestCase(TestCase):
    def test_configuration(self):
        self.assertIsNotNone(config.BASE_DIR)
        self.assertIsNotNone(config.CONFIG_PATH)
        self.assertIsNotNone(config.MEDIA_PATH)
        self.assertIsNotNone(config.DB_PATH)
        self.assertIsNotNone(config.DB_DRIVER)
        self.assertIsNotNone(config.DB_NAME)
        self.assertIsNotNone(config.SECRET_KEY)
        self.assertIsNotNone(config.DATABASE_URL)
        self.assertIsNotNone(config.JW_TOKEN_MINUTES_LIVE)
        self.assertIsNotNone(config.DATABASE_TEST_URL)
        self.assertIsNotNone(config.DB_TEST_NAME)
        self.assertNotEqual(config.DATABASE_TEST_URL, config.DATABASE_URL, "test database must have another path")

    def test_internet_connection(self):
        import requests
        google = 'https://www.google.com/'
        try:
            requests.get(google)
        except Exception as e:
            print(e)
            self.fail('check internet connection')

    def test_database_existing(self):
        pass

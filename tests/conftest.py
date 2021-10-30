from unittest import TestCase

from flask_sqlalchemy import SQLAlchemy

import config.routes
from config.run_config import app


class BaseTestCase(TestCase):
    def create_app(self):
        print('test app configured')
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = config.config.DATABASE_TEST_URL

        return app

    def setUp(self):
        self.db_control_test = SQLAlchemy(self.create_app())
        self.db_control_test.create_all()

    def tearDown(self) -> None:
        self.db_control_test.session.remove()
        self.db_control_test.drop_all()

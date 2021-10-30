import json

import config.routes
from tests.conftest import BaseTestCase


class ConfigTestCase(BaseTestCase):
    def test_registration_get_valid(self):
        app = self.create_app()

        response = app.test_client().post(config.routes.REGISTER, json=dict(name='ivan', password='dafsjkd111'))
        print(response)
        assert (response.status_code == 200)

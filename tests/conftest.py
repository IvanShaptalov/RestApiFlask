import pytest

import config.config
from app.api import create_app


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    # create the app with common test config
    print('fixture working?')
    app = create_app(test_config={"TESTING": True, "DATABASE": config.config.DATABASE_TEST_URL})

    return app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

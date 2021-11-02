import pytest

from config import routes


@pytest.mark.profile
def test_change_name_valid(client, token, delete_aliases_caller, change_username):
    """testing registration in valid case, expected 201"""
    try:
        headers = {'x-access-tokens': token}
        response = client.put(routes.PROFILE_PREFIX + routes.USERNAME, json=change_username, headers=headers)
        assert response.status_code == 201, "expected 201, username not changed"
    finally:
        delete_aliases_caller()



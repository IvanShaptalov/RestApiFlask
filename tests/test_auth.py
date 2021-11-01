import pytest


@pytest.mark.auth
def test_index_html(client):
    response = client.get('/')
    assert response.status_code == 200, "index don`t work correctly"

import pytest

from config import routes


@pytest.mark.auth
def test_index_html(client):
    response = client.get('/')
    assert response.status_code == 200, "index don`t work correctly"


@pytest.mark.auth
def test_registration_valid(client, registration_data, delete_aliases_caller):
    """test registration in valid case, expected 201"""
    try:
        response = client.post(routes.AUTH_PREFIX + routes.REGISTER, json=registration_data)
        if len(response.headers) > 0:
            print(response.headers[0])
        assert response.status_code == 201, "expected 201, user creating"
    finally:
        delete_aliases_caller()


@pytest.mark.auth
def test_user_unique_in_registration(client, registration_data, delete_aliases_caller):
    """test user unique while registration"""
    try:
        response1 = client.post(routes.AUTH_PREFIX + routes.REGISTER, json=registration_data)
        response2 = client.post(routes.AUTH_PREFIX + routes.REGISTER, json=registration_data)
        assert response1.status_code == 201, "expected 201, user creating"
        assert response2.status_code == 400, "expected 400, user already created"
    finally:
        delete_aliases_caller()


@pytest.mark.auth
def test_two_user_creating(client, registration_data, registration_data_1, delete_aliases_caller):
    try:
        response1 = client.post(routes.AUTH_PREFIX + routes.REGISTER, json=registration_data)
        response2 = client.post(routes.AUTH_PREFIX + routes.REGISTER, json=registration_data_1)
        assert response1.status_code == 201, "expected 201, user creating"
        assert response2.status_code == 201, "expected 201, user creating"
        response1 = client.post(routes.AUTH_PREFIX + routes.REGISTER, json=registration_data)
        response2 = client.post(routes.AUTH_PREFIX + routes.REGISTER, json=registration_data_1)
        assert response1.status_code == 400, "expected 400, user already created"
        assert response2.status_code == 400, "expected 400, user already created"
    finally:
        delete_aliases_caller()


@pytest.mark.auth
def test_registration_password_missed(client, r_data_pass_missed, delete_aliases_caller):
    try:
        response1 = client.post(routes.AUTH_PREFIX + routes.REGISTER, json=r_data_pass_missed)
        assert response1.status_code == 400, "user password have bug while filtering or saving"
    finally:
        delete_aliases_caller()


@pytest.mark.auth
def test_registration_password_weak(client, r_data_pass_weak, delete_aliases_caller):
    try:
        for index, data in enumerate(r_data_pass_weak):
            response1 = client.post(routes.AUTH_PREFIX + routes.REGISTER, json=data)
            assert response1.status_code == 400, f"user password have bug while filtering or saving: {data}"
            print(f'case# {index} ok')
    finally:
        delete_aliases_caller()


def test_name_invalid(client, r_data_name_invalid, delete_aliases_caller):
    try:

        for index, data in enumerate(r_data_name_invalid):
            response1 = client.post(routes.AUTH_PREFIX + routes.REGISTER, json=data)
            assert response1.status_code == 400, f"user password have bug while filtering or saving: {data}"
            print(f'case #{index} ok')
    finally:
        delete_aliases_caller()

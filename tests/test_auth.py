import pytest
from config import routes
from tests.conftest import login_headers


# region index testing

@pytest.mark.auth
def test_index_html(client):
    response = client.get('/')
    assert response.status_code == 200, "index don`t work correctly"


# endregion index testing

# region registration tests
@pytest.mark.auth
def test_registration_valid(client, registration_data, delete_aliases_caller):
    """testing registration in valid case, expected 201"""
    try:
        response = client.post(routes.AUTH_PREFIX + routes.REGISTER, json=registration_data)
        if len(response.headers) > 0:
            print(response.headers[0])
        assert response.status_code == 201, "expected 201, user creating"
    finally:
        delete_aliases_caller()


@pytest.mark.auth
def test_user_unique_in_registration(client, registration_data, delete_aliases_caller):
    """testing user unique while registration"""
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


@pytest.mark.auth
def test_name_invalid(client, r_data_name_invalid, delete_aliases_caller):
    try:

        for index, data in enumerate(r_data_name_invalid):
            response1 = client.post(routes.AUTH_PREFIX + routes.REGISTER, json=data)
            assert response1.status_code == 400, f"user password have bug while filtering or saving: {data}"
            print(f'case #{index} ok')
    finally:
        delete_aliases_caller()


# endregion registration tests

# region login tests


@pytest.mark.auth
def test_login_missed_username(client, registration_data, delete_aliases_caller):
    try:
        # create user
        response = client.post(routes.AUTH_PREFIX + routes.REGISTER, json=registration_data)
        if len(response.headers) > 0:
            print(response.headers[0])
        assert response.status_code == 201, "expected 201, user creating"

        response = client.post(routes.AUTH_PREFIX + routes.LOGIN, headers=login_headers(missed_username=True))
        print(response)
        assert response.status_code == 401, "username filter not work"
    finally:
        delete_aliases_caller()


@pytest.mark.auth
def test_login_missed_password(client, registration_data, delete_aliases_caller):
    try:
        # create user
        response = client.post(routes.AUTH_PREFIX + routes.REGISTER, json=registration_data)
        if len(response.headers) > 0:
            print(response.headers[0])
        assert response.status_code == 201, "expected 201, user creating"

        response = client.post(routes.AUTH_PREFIX + routes.LOGIN, headers=login_headers(missed_password=True))
        print(response)
        assert response.status_code == 401, "username filter not work"
    finally:
        delete_aliases_caller()

# endregion login tests

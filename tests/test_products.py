import pytest

import config.routes


@pytest.mark.products
def test_product_creating(token, client, delete_aliases_caller, product_valid):
    try:
        headers = {'x-access-tokens': token}
        response = client.post(config.routes.PRODUCT_PREFIX, headers=headers, json=product_valid)
        assert response.status_code == 201, "product is not created"
    finally:
        delete_aliases_caller()


@pytest.mark.products
def test_product_creating_invalid(token, client, delete_aliases_caller, products_invalid):
    try:
        for product in products_invalid:
            headers = {'x-access-tokens': token}
            response = client.post(config.routes.PRODUCT_PREFIX, headers=headers, json=product)
            assert response.status_code == 400, "created invalid product"
    finally:
        delete_aliases_caller()


@pytest.mark.products
def test_get_products_valid(token, client, delete_aliases_caller):
    try:
        headers = {'x-access-tokens': token}
        response = client.get(config.routes.PRODUCT_PREFIX, headers=headers)
        assert response.status_code == 200
    finally:
        delete_aliases_caller()


@pytest.mark.products
def test_get_products_invalid(client, delete_aliases_caller):
    try:
        response = client.get(config.routes.PRODUCT_PREFIX)
        assert response.status_code == 400
    finally:
        delete_aliases_caller()
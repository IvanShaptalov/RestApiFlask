import pytest
import config


@pytest.mark.products
def test_product_creating(token, client, delete_aliases_caller, product_valid):
    try:
        headers = {'x-access-tokens': token}
        response = client.post(config.routes.PRODUCT_PREFIX, headers=headers, json=product_valid)
        assert response.status_code == 201, "product is not created"
    finally:
        delete_aliases_caller()


@pytest.mark.products
def test_product_pagination(client, delete_aliases_caller, pagination_args):
    try:
        response = client.get(config.routes.PRODUCT_PREFIX+pagination_args)
        assert response.status_code == 200, "pagination don't work correctly"
    finally:
        delete_aliases_caller()

# test filtering

# test sorting

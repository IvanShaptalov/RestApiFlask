import pytest

import config


@pytest.mark.currency
def test_add_currency_valid(token, client, delete_aliases_caller, product_valid, valid_pricelist):
    try:
        headers = {'x-access-tokens': token}
        response = client.post(config.routes.PRODUCT_PREFIX, headers=headers, json=product_valid)
        assert response.status_code == 201, "product is not created"
        for price in valid_pricelist:
            headers = {'x-access-tokens': token, 'product-article': product_valid['article']}
            response = client.post(config.routes.PRICE_PREFIX, headers=headers, json=price)
            assert response.status_code == 201, f"price is not added {price}"
    finally:
        delete_aliases_caller()


@pytest.mark.currency
def test_add_currency_invalid(token, client, delete_aliases_caller, product_valid, invalid_pricelist):
    try:
        headers = {'x-access-tokens': token}
        response = client.post(config.routes.PRODUCT_PREFIX, headers=headers, json=product_valid)
        assert response.status_code == 201, "product is not created"
        for price in invalid_pricelist:
            headers = {'x-access-tokens': token, 'product-article': product_valid['article']}
            response = client.post(config.routes.PRICE_PREFIX, headers=headers, json=price)
            assert response.status_code == 400, f"invalid price added {price}"
    finally:
        delete_aliases_caller()


@pytest.mark.currency
def test_add_currency_unique(token, client, delete_aliases_caller, product_valid, pricelist_unique_failed):
    try:
        headers = {'x-access-tokens': token}
        response = client.post(config.routes.PRODUCT_PREFIX, headers=headers, json=product_valid)
        assert response.status_code == 201, "product is not created"
        for price, response_code in zip(pricelist_unique_failed, [201, 400]):
            headers = {'x-access-tokens': token, 'product-article': product_valid['article']}
            response = client.post(config.routes.PRICE_PREFIX, headers=headers, json=price)
            assert response.status_code == response_code, f"unique test failed {price}"
    finally:
        delete_aliases_caller()
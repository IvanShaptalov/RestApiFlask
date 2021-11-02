from flask import Blueprint, jsonify, request, make_response

import config
from app.models import Price, Product, db_util
from app.security.token_provider import token_required, product_required
from app.filters import filter

bp = Blueprint('price', __name__, url_prefix=config.routes.PRICE_PREFIX)


@bp.post('')
@token_required
@product_required
@filter.data_exists(['currency', 'count'])
def create_currency(product: Product):
    print('passed')
    print(product)
    data = request.get_json()
    assert isinstance(data, dict)
    currency, count = data['currency'], data['count']
    # region filters
    if not filter.check_is_digit(count, above_zero=True):
        return make_response('bad request', 400,
                             {'Number error': 'price is not number or below zero'})

    if db_util.check_unique_value_in_table(session_p=db_util.sc_session,
                                           table_class=Price,
                                           identifier_to_value=[Price.product_id == product.id,
                                                                Price.currency == currency]):
        return make_response('bad request', 400,
                             {'Unique error': 'current product already exist'})
    # endregion filters

    # add price to user
    db_util.write_obj_to_table(session_p=db_util.sc_session,
                               table_class=Price,
                               identifier_to_value=[Price.product_id == product.id,
                                                    Price.currency == currency],
                               currency=currency,
                               count=count,
                               product_id=product.id)
    return jsonify({'Created': {'article': product.article, 'name': product.name}}), 201

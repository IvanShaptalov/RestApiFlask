from flask import Blueprint, request

import config
from app.models import Price, Product, db_util
from app.security.token_provider import token_required, product_required
from app.filters import filter
from app.utils import resp_shortcut

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
        return resp_shortcut(message='Bad request',
                             desc='login Price is not number or below zero',
                             code=400)
    with db_util.sc_session as session:
        if db_util.check_unique_value_in_table(session_p=session,
                                               table_class=Price,
                                               identifier_to_value=[Price.product_id == product.id,
                                                                    Price.currency == currency]):
            return resp_shortcut(message='Bad request',
                                 desc='current product already exist',
                                 code=400)
        # endregion filters

        # add price to user
        db_util.write_obj_to_table(session_p=session,
                                   table_class=Price,
                                   identifier_to_value=[Price.product_id == product.id,
                                                        Price.currency == currency],
                                   currency=currency,
                                   count=count,
                                   product_id=product.id)
    return resp_shortcut(message='Created',
                         desc=f'{count} {currency} added to product',
                         code=201)

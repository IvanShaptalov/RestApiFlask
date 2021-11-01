import config.validation_config
from app.models import Product, User, db_util
from app.security.token_provider import token_required
from flask import request, make_response, Blueprint

from app.filters import filter

bp = Blueprint('product', __name__, url_prefix='/product')


@bp.route('/create', methods=['POST', 'GET'])
@token_required
@filter.data_exists(['article', 'name'])
def create_product(current_user: User):
    data = request.get_json()
    if db_util.check_unique_value_in_table(session=db_util.sc_session,
                                           table_class=Product,
                                           identifier_to_value=[Product.user_id == current_user.id,
                                                                Product.article == data['article']]):
        return make_response('bad request', 400,
                             {'Unique error': 'current product already exist'})
    if not filter.check_args_length(data['article'],
                                    min_len=config.validation_config.MIN_ARTICLE_LENGTH,
                                    max_len=config.validation_config.MAX_ARTICLE_LENGTH):
        return make_response('bad request', 400,
                             {'Unique error': 'bad article length'})

    new_product = Product(article=data['article'],
                          name=data['name'],
                          user_id=current_user.id)
    db_util.write_obj_to_table(session_p=db_util.sc_session,
                               table_class=Product,
                               identifier_to_value=[Product.article == data['article']],
                               name=data['name'],
                               article=data['article'],
                               user_id=current_user.id)

    return make_response('created', 201,
                         {'Created': 'product created'})


# @app.route('/products', methods=['POST', 'GET'])
# @token_required
# def get_products(current_user):
#     products = Product.query.filter_by(user_id=current_user.id)
#     output = []
#     for product in products:
#         assert isinstance(product, Product)
#         # create pricelist
#         pricelist = []
#         for price in product.pricelist:
#             assert isinstance(price, Price)
#             price_data = {
#                 'currency': price.currency,
#                 'count': price.count
#             }
#             pricelist.append(price_data)
#         # create product
#         product_data = {'article': product.article,
#                         'name': product.name,
#                         'pricelist': pricelist}
#         output.append(product_data)
#     return jsonify({'list_of_products': output})

print('product bind')

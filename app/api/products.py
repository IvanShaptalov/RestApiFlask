import config.validation_config
from app.models.db_util import Product, sc_session, User
from app.security.token_provider import token_required
from config.run_config import app
from flask import request, make_response
from app.filters import filter


@app.route('/create_product', methods=['POST', 'GET'])
@token_required
@filter.data_exists(['article', 'name'])
def create_product(current_user: User):
    data = request.get_json()
    if filter.check_unique_value_in_table(Product,
                                          [Product.user_id == current_user.id, Product.article == data['article']]):
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
    sc_session.add(new_product)
    sc_session.commit()

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

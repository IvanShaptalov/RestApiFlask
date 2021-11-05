import config.validation_config
from app.models import Product, User, db_util
from app.security.token_provider import token_required
from flask import request
from flask_rest_api import Blueprint

from app.filters import filter
from app.utils import resp_shortcut

bp = Blueprint('product', __name__, url_prefix=config.routes.PRODUCT_PREFIX)
from app.api import product_list

print(f'import module {product_list}')


@bp.post('')
@token_required
@filter.data_exists(['article', 'name'])
def create_product(current_user: User):
    data = request.get_json()
    with db_util.sc_session as session:

        if db_util.check_unique_value_in_table(session_p=session,
                                               table_class=Product,
                                               identifier_to_value=[Product.user_id == current_user.id,
                                                                    Product.article == data['article']]):

            return resp_shortcut(message='Bad request',
                                 desc='current product already exist',
                                 code=400)
        if not filter.check_args_length(data['article'],
                                        min_len=config.validation_config.MIN_ARTICLE_LENGTH,
                                        max_len=config.validation_config.MAX_ARTICLE_LENGTH):
            return resp_shortcut(message='Bad request',
                                 desc='invalid article',
                                 code=400)

        new_product = Product(article=data['article'],
                              name=data['name'],
                              user_id=current_user.id)
        db_util.write_obj_to_table(session_p=session,
                                   table_class=Product,
                                   identifier_to_value=[Product.article == data['article']],
                                   name=data['name'],
                                   article=data['article'],
                                   user_id=current_user.id)

        return resp_shortcut(message='Created',
                             desc='product created',
                             code=201)

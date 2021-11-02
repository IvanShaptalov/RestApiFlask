from flask import request, current_app
import jwt
from functools import wraps

from app import models
from app.models import db_util
from app.utils import response_util


def token_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):

        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return response_util(code=400, message='Bad request', desc='a valid token is missing')

        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = db_util.sc_session.query(models.User).filter_by(public_id=payload['public_id']).first()
        except Exception as e:
            print(type(e), e)
            return response_util(code=401, message='Unauthorized', desc='token is invalid or expired')
        return func(current_user, *args, **kwargs)

    return decorator


def product_required(func):
    @wraps(func)
    def decorator(current_user, *args, **kwargs):
        article = None
        if 'product-article' in request.headers:
            article = request.headers['product-article']

        if not article:
            return response_util(code=400, message='Bad request', desc='product article is missing')

        try:
            product = db_util.get_from_db_multiple_filter(open_session=db_util.sc_session,
                                                          table_class=models.Product,
                                                          identifier_to_value=[
                                                              models.Product.user_id == current_user.id,
                                                              models.Product.article == article])
        except Exception as e:
            print(type(e), e)
            return response_util(code=400, message='Bad request', desc='product with article not exists')
        return func(product, *args, **kwargs)

    return decorator

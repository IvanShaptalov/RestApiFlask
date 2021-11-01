from flask import request, jsonify, current_app
import jwt
from functools import wraps

from app import models
from app.models import User, db_util


def token_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = db_util.sc_session.query(models.User).filter_by(public_id=payload['public_id']).first()
        except Exception as e:
            print(type(e), e)
            return jsonify({'message': 'token is invalid or expired'})
        return func(current_user, *args, **kwargs)
    return decorator



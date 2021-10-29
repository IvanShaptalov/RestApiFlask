from functools import wraps
from flask import request, jsonify
import re

import config.validation_config
from app.models.db_util import User


def data_exists(key_list: list):
    """
    check is request have values from data_list
    :param key_list: list of values to check existing in request
    """

    def decorator(func):

        @wraps(func)
        def wrapper():
            data = request.get_json()
            for key in key_list:
                if key not in data:
                    return jsonify({'bad request': 400, 'Arguments missed': 'name or password required'})
            return func()

        return wrapper

    return decorator


def check_password_validity(password) -> bool:
    """
    check that password have letter, number and special character;
    password min length = 8;

    :param password: value to check validity
    :return:
    """
    if re.fullmatch(config.validation_config.PASSWORD_PATTERN, password):
        return True
    else:
        return False


# no match


def check_user_unique(username):
    # if username empty

    return not (isinstance(User.query.filter_by(username=username).first(), User))


def check_args_length(*args, min_len):
    for arg in args:
        if len(arg) < min_len:
            return False
    return True

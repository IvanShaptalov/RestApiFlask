from functools import wraps
from flask import request, jsonify
import re

import config.validation_config


def data_exists(key_list: list):
    """
    check is request have values from data_list
    :param key_list: list of values to check existing in request
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.get_json()
            for key in key_list:
                if key not in data:
                    return jsonify(
                        {'bad request': 400, 'Arguments missed': 'expected some of arguments, but not given'})
            return func(*args, **kwargs)

        return wrapper

    return decorator


def check_password_validity(password) -> bool:
    """
    check that password have letter, number and special character;
    password min length = 8;

    :param password: value to check validity
    :return: True if password valid
    """
    if re.fullmatch(config.validation_config.PASSWORD_PATTERN, password):
        return True
    else:
        return False


# no match


def check_unique_value_in_table(model, identifier_to_value: list):
    """
    check unique in table
    :param model: sqlalchemy model,
    :param identifier_to_value: instrumented attribute to value, example [User.id == 5, User.name = 'abc']
    :return: True if object exists in table
    """
    # if username empty
    obj = model.query.filter(*identifier_to_value).first()
    return obj is not None


def check_args_length(*args, min_len, max_len):
    """
    :param args: values to validation
    :param min_len: min len
    :param max_len: max len
    :return: True if argument is valid
    """
    for arg in args:
        if max_len:
            if len(arg) > max_len:
                return False
        if len(arg) < min_len:
            return False
    return True

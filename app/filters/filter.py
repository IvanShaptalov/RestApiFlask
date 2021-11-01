from functools import wraps
from flask import request, make_response
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
            def bad_request(error, desc):
                return make_response('bad request', 400,
                                     {error: desc})

            # get json
            data = request.get_json()
            # check if json is dictionary
            if not isinstance(data, dict):
                return bad_request(error='Json warning', desc=f'expected dictionary from json, given: {type(data)}')
            for key in key_list:
                if key not in data:
                    return bad_request(error='Arguments missed', desc='expected some of arguments, but not given')
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

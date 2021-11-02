from functools import wraps
from flask import request
import re

import config.validation_config
from app.utils import response_util


def data_exists(key_list: list):
    """
    check is request have values from data_list
    :param key_list: list of values to check existing in request
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            # get json
            data = request.get_json()
            # check if json is dictionary
            if not isinstance(data, dict):
                return response_util(message='Json warning', desc=f'expected dictionary from json, given: {type(data)}', code=400)
            for key in key_list:
                if key not in data:
                    return response_util(message='Arguments missed', desc='expected some of arguments, but not given', code=400)
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


def check_is_digit(*args, above_zero: bool = False, below_zero: bool = False):
    """:return True if all args is digits"""
    if above_zero or below_zero:
        assert above_zero != below_zero, "how number can be above and below zero at the same time?"

    for arg in args:
        try:
            # check that arg can be str
            str(arg)
        except Exception as e:
            print(type(e), e)
            return False
        else:
            # check that arg is digit
            try:
                num = float(arg)
            except ValueError as e:
                return False
            # check that num above zero if required
            if above_zero:
                if num <= 0:
                    return False
            # check that num below zero if required
            if below_zero:
                if num >= 0:
                    return False

    return True

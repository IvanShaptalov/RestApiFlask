from functools import wraps
from flask import request
import re

import config.validation_config
from app.models import db_util, User
from app.utils import resp_shortcut


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
                return resp_shortcut(message='Bad request', desc=f'expected dictionary from json, given: {type(data)}',
                                     code=400)
            for key in key_list:
                if key not in data:
                    return resp_shortcut(message='Arguments missed', desc='expected some of arguments, but not given',
                                         code=400)
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


def allowed_file(filename):
    """:return True if given file have valid extension """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.validation_config.ALLOWED_EXTENSIONS


def image_exists():
    """:return True if file exist"""
    return 'image' in request.files


def user_filter(data, password_required=True):
    # region filtering
    min_l = config.validation_config.MIN_NAME_LENGTH
    max_l = config.validation_config.MAX_NAME_LENGTH

    if not check_args_length(data['name'], min_len=min_l, max_len=max_l):
        return resp_shortcut(message='Bad request',
                             desc=f'username at least {min_l} characters',
                             code=400)

    if db_util.check_unique_value_in_table(db_util.sc_session,
                                           table_class=User,
                                           identifier_to_value=[User.username == data['name']]):
        return resp_shortcut(message='Bad request',
                             desc='user with current name already exist',
                             code=400)
    if password_required:
        if not check_password_validity(data['password']):
            return resp_shortcut(message='Bad request',
                                 desc='weak password',
                                 code=400)
    # endregion filtering

from datetime import datetime

from flask import make_response
from os.path import splitext


def resp_shortcut(message, desc, code):
    return make_response(message, code,
                         {'description': desc})


def get_timestamp_path(filename):
    return '{}{}'.format(datetime.now().timestamp(), splitext(filename)[1])

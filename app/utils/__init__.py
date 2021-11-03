from datetime import datetime

from flask import jsonify
from os.path import splitext


def resp_shortcut(message, desc, code):
    return jsonify({'message': message, 'desc': desc}), code


def get_timestamp_path(filename):
    return '{}{}'.format(datetime.now().timestamp(), splitext(filename)[1])

from flask import make_response


def response_util(message, desc, code):
    return make_response('bad request', code,
                         {message: desc})
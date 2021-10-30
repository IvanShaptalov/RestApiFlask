import config.config
from app.models.db_util import User, sc_session
from config.run_config import app
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from app.filters import filter


@app.route(config.routes.REGISTER, methods=['POST'])
@filter.data_exists(key_list=['name', 'password'])
def signup_user():
    data = request.get_json()
    # region filtering
    min_l = config.validation_config.MIN_NAME_LENGTH
    max_l = config.validation_config.MAX_NAME_LENGTH
    if not filter.check_args_length(data['name'], min_len=min_l, max_len=max_l):
        return make_response('bad request', 400,
                             {'Validation error': f'username at least {min_l} characters'})

    if filter.check_unique_value_in_table(model=User,
                                          identifier_to_value=[User.username == data['name']]):
        return make_response('bad request', 400,
                             {'Unique error': 'user with current name already exist'})

    if not filter.check_password_validity(data['password']):
        return make_response('bad request', 400,
                             {'Security warning': 'weak password'})
    # endregion filtering

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()),
                    username=data['name'],
                    password=hashed_password)
    sc_session.add(new_user)
    sc_session.commit()
    return make_response('registered', 201,
                         {'WWW.Authentication': 'register successful'})


@app.route(config.routes.LOGIN, methods=['POST'])
def login_user():
    auth = request.authorization
    # region filtering
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
    user = User.query.filter_by(username=auth.username).first()
    if user is None:
        return make_response('could not verify', 401,
                             {'WWW.Authentication': 'Basic realm: "invalid login or password"'})
    # endregion
    if check_password_hash(user.password, auth.password):
        token_live = config.config.JW_TOKEN_MINUTES_LIVE
        expired = datetime.datetime.utcnow() + datetime.timedelta(minutes=token_live)

        token = jwt.encode({'public_id': user.public_id, 'exp': expired},
                           app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({'token': token})
    return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

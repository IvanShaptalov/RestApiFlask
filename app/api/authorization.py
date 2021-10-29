import config.config
from app.models.db_util import User, session
from config.run_config import app
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from app.filters import filter


@app.route('/register', methods=['GET', 'POST'])
@filter.data_exists(key_list=['name', 'password'])
def signup_user():
    data = request.get_json()
    # region filtering
    min_l = config.validation_config.MIN_USERNAME_LENGTH
    if not filter.check_args_length(data['name'], min_len=min_l):
        return jsonify({'Validation error': f'username at least {min_l} characters',
                        'bad request': 400})

    if not filter.check_user_unique(data['name']):
        return jsonify({'Unique warning': 'user with current name already exist',
                        'bad request': 400})

    if not filter.check_password_validity(data['password']):
        return jsonify({'Security warning': 'weak password',
                        'bad request': 400})
    # endregion filtering

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()),
                    username=data['name'],
                    password=hashed_password)
    session.add(new_user)
    session.commit()
    return jsonify({'message': 'registered successfully'})


@app.route('/login', methods=['GET', 'POST'])
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

        token = jwt.encode({'public_id': user.public_id,
                            'exp': expired},
                           app.config['SECRET_KEY'])
        return jsonify({'token': token})
    return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

import config.config
from app import models
from app.filters.filter import user_filter
from app.models import User, db_util
from flask import request, jsonify, make_response, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from app.filters import filter

bp = Blueprint('register', __name__, url_prefix='/auth')


@bp.post(config.routes.REGISTER)
@filter.data_exists(key_list=['name', 'password'])
def signup_user():
    data = request.get_json()

    filter_result = user_filter(data)
    if filter_result is not None:
        return filter_result
    hashed_password = generate_password_hash(data['password'], method='sha256')

    db_util.write_obj_to_table(session_p=db_util.sc_session,
                               table_class=models.User,
                               public_id=str(uuid.uuid4()),
                               username=data['name'],
                               password=hashed_password)
    return make_response('registered', 201,
                         {'WWW.Authentication': 'register successful'})


@bp.post(config.routes.LOGIN)
def login_user():
    auth = request.authorization

    # region filtering
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = db_util.sc_session.query(User).filter_by(username=auth.username).first()
    if user is None:
        return make_response('could not verify', 401,
                             {'WWW.Authentication': 'Basic realm: "invalid login or password"'})
    # endregion
    if check_password_hash(user.password, auth.password):
        token_live = config.config.JW_TOKEN_MINUTES_LIVE
        expired = datetime.datetime.utcnow() + datetime.timedelta(minutes=token_live)

        token = jwt.encode({'public_id': user.public_id, 'exp': expired},
                           config.config.SECRET_KEY, algorithm="HS256")

        return jsonify({'token': token})
    return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})


print('auth bind')

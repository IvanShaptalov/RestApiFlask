import app.utils
import config.config
from app import models
from app.filters.filter import user_filter
from app.models import User, db_util
from flask import request, jsonify, Blueprint
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
    return app.utils.resp_shortcut(message='WWW.Authentication', desc='register successful', code=201)


@bp.post(config.routes.LOGIN)
def login_user():
    auth = request.authorization

    # region filtering
    if not auth or not auth.username or not auth.password:
        return app.utils.resp_shortcut(message='WWW.Authentication Basic realm',
                                       desc='login required',
                                       code=401)

    user = db_util.sc_session.query(User).filter_by(username=auth.username).first()
    if user is None:
        return app.utils.resp_shortcut(message='WWW.Authentication Basic realm',
                                       desc='invalid login or password',
                                       code=401)
    # endregion
    if check_password_hash(user.password, auth.password):
        token_live = config.config.JW_TOKEN_MINUTES_LIVE
        expired = datetime.datetime.utcnow() + datetime.timedelta(minutes=token_live)

        token = jwt.encode({'public_id': user.public_id, 'exp': expired},
                           config.config.SECRET_KEY, algorithm="HS256")

        return jsonify({'token': token})
    return app.utils.resp_shortcut(message='WWW.Authentication Basic realm',
                                   desc='login required',
                                   code=401)


print('auth bind')

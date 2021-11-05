import os

from werkzeug.utils import secure_filename

import config.validation_config
from app import utils
from app.filters.filter import user_filter
from app.models import User, db_util
from app.security.token_provider import token_required
from flask import request, Blueprint, send_file
from app.filters import filter
from app.utils import resp_shortcut

bp = Blueprint('profile', __name__, url_prefix=config.routes.PROFILE_PREFIX)


@bp.post(config.routes.IMAGE)
@token_required
def upload_image(current_user: User):
    # region filters
    print(request.files)
    if not filter.image_exists():
        return resp_shortcut(message='bad request', code=400, desc='image missed')
    if 'image' not in request.files and not filter.allowed_file(request.files['image'].filename):
        return resp_shortcut(message='bad request', code=400,
                             desc=f'allowed extensions: {config.validation_config.ALLOWED_EXTENSIONS}')

    # endregion filters
    try:
        image = request.files['image']
        filename = utils.get_timestamp_path(secure_filename(image.filename))
        image.save(os.path.join(config.config.MEDIA_PATH, filename))
    except Exception as e:
        print(type(e), e)
    else:
        avatar_path = current_user.avatar_path
        if avatar_path:
            try:
                os.remove(os.path.join(config.config.MEDIA_PATH, avatar_path))
                print('file removed')
            except OSError:
                pass
        with db_util.sc_session as session:
            db_util.edit_obj_in_table(session_p=session,
                                      table_class=User,
                                      identifier_to_value=[User.id == current_user.id],
                                      avatar_path=filename)
            return resp_shortcut(message='created', code=201, desc='image uploaded')
    return resp_shortcut(message='bad request', code=400, desc='image not valid')


@bp.get(config.routes.IMAGE)
@token_required
def get_image(current_user: User):
    if current_user.avatar_path:
        return send_file(os.path.join(config.config.MEDIA_PATH, current_user.avatar_path))
    return resp_shortcut('resource not found', 'this file dont exist', 404)


# region later
@bp.put(config.routes.USERNAME)
@token_required
@filter.data_exists(['name'])
def change_username(current_user: User):
    data = request.get_json()
    # user filter
    filter_result = user_filter(data=data, password_required=False)
    if filter_result is not None:
        return filter_result
    with db_util.sc_session as session:
        db_util.edit_obj_in_table(session_p=session,
                                  table_class=User,
                                  identifier_to_value=[User.id == current_user.id],
                                  username=data['name'])

    return resp_shortcut(message='WWW.Authentication',
                         desc='register successful',
                         code=201)
# endregion

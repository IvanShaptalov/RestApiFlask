from app.models.db_util import User
from config.run_config import app
from flask import jsonify


@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()

    result = []
    for user in users:
        if isinstance(user, User):
            user_data = {'public_id': user.public_id,
                         'username': user.username,
                         'password': user.password,
                         'path': user.avatar_path}

            result.append(user_data)

    return jsonify({'users': result})

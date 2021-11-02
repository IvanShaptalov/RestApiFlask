from icecream import ic

import config.config
from config.config import SECRET_KEY, DATABASE_URL
import os
from flask import Flask


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True, root_path=config.config.BASE_DIR)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY=SECRET_KEY,
        # store the database in the instance folder
        DATABASE=DATABASE_URL,
    )

    # load the config if passed in
    ic(test_config)
    if test_config:
        print('test')
        print('test ', test_config)
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def hello():
        return "Hello, World!"

    # register the database commands
    from app.models import db_util
    with app.app_context():
        db_util.init_app(app)

    # apply the blueprints to the app
    from . import products
    from . import auth
    from . import currency

    app.register_blueprint(auth.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(currency.bp)

    return app

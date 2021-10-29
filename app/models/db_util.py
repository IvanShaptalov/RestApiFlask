from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker

import config.validation_config
from config.run_config import app

db_control = SQLAlchemy(app)
sc_session = scoped_session(sessionmaker(bind=db_control.engine))
# test database


# region models
class User(db_control.Model):
    id = db_control.Column(db_control.Integer, primary_key=True, index=True, autoincrement='auto')
    public_id = db_control.Column(db_control.Integer)
    username = db_control.Column(db_control.String(config.validation_config.MAX_NAME_LENGTH), unique=True)
    password = db_control.Column(db_control.String(config.validation_config.MAX_PASSWORD_LENGTH), unique=False)
    avatar_path = db_control.Column(db_control.String(config.validation_config.MAX_AVATAR_PATH_LENGTH), unique=False)
    products = db_control.relationship('Product', backref='user', lazy=True)

    def __str__(self):
        return f'{self.username}'


class Product(db_control.Model):
    id = db_control.Column(db_control.Integer, primary_key=True, index=True, autoincrement='auto')
    # todo how make article unique to each other but other in current user?
    name = db_control.Column(db_control.String(config.validation_config.MAX_NAME_LENGTH))
    article = db_control.Column(db_control.String(config.validation_config.MAX_ARTICLE_LENGTH))
    user_id = db_control.Column(db_control.Integer, db_control.ForeignKey('user.id'))
    pricelist = db_control.relationship('Price', backref='product', lazy=True)


class Price(db_control.Model):
    id = db_control.Column(db_control.Integer, primary_key=True, index=True, autoincrement='auto')
    currency = db_control.Column(db_control.String(config.validation_config.MAX_CURRENCY_LENGTH))
    count = db_control.Column(db_control.BigInteger)
    product_id = db_control.Column(db_control.Integer, db_control.ForeignKey('product.id'))


def create_all():
    db_control.create_all()
    print('db created')
# endregion

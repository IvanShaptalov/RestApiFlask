from flask_sqlalchemy import SQLAlchemy
from config.run_config import app

db_obj = SQLAlchemy(app)


# test database


# region models
class User(db_obj.Model):
    user_id = db_obj.Column(db_obj.Integer, primary_key=True, index=True, autoincrement='auto')
    username = db_obj.Column(db_obj.String(50), unique=True)
    avatar_path = db_obj.Column(db_obj.String(200), unique=False)
    products = db_obj.relationship('Product', backref='user', lazy=True)

    def __str__(self):
        return f'{self.username}'


class Product(db_obj.Model):
    product_id = db_obj.Column(db_obj.Integer, primary_key=True, index=True, autoincrement='auto')
    # todo how make article unique to each other but other in current user?
    article = db_obj.Column(db_obj.String(100))
    user_id = db_obj.Column(db_obj.Integer, db_obj.ForeignKey('user.user_id'))
    pricelist = db_obj.relationship('Price', backref='product', lazy=True)


class Price(db_obj.Model):
    price_id = db_obj.Column(db_obj.Integer, primary_key=True, index=True, autoincrement='auto')
    currency = db_obj.Column(db_obj.String(50))
    count = db_obj.Column(db_obj.BigInteger)
    product_id = db_obj.Column(db_obj.Integer, db_obj.ForeignKey('product.product_id'))


def create_all():
    db_obj.create_all()
    print('db created')
# endregion

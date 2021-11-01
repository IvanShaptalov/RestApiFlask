from sqlalchemy import Column, String, Integer, ForeignKey, BigInteger
from sqlalchemy.orm import declarative_base, relationship

from config import validation_config

print('base')
Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    public_id = Column(Integer)
    username = Column(String(validation_config.MAX_NAME_LENGTH), unique=True)
    password = Column(String(validation_config.MAX_PASSWORD_LENGTH), unique=False)
    avatar_path = Column(String(validation_config.MAX_AVATAR_PATH_LENGTH), unique=False)

    products = relationship('Product', backref='user', lazy=True)

    def __str__(self):
        return f'{self.username}'


class Product(Base):
    __tablename__ = "product"
    id = Column('id', Integer, primary_key=True, index=True, autoincrement='auto')
    # todo how make article unique to each other but other in current user?
    name = Column('name', String(validation_config.MAX_NAME_LENGTH))
    article = Column('article', String(validation_config.MAX_ARTICLE_LENGTH))
    user_id = Column('user_id', Integer, ForeignKey('user.id'))
    pricelist = relationship('Price', backref='product', lazy=True)


class Price(Base):
    __tablename__ = "price"
    id = Column('id', Integer, primary_key=True, index=True, autoincrement='auto')
    currency = Column('currency', String(validation_config.MAX_CURRENCY_LENGTH))
    count = Column('count', BigInteger)
    product_id = Column('product_id', Integer, ForeignKey('product.id'))

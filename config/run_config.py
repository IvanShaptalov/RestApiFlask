from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from config import config

print('run config')

app = Flask(__name__)
# database
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
# security
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

test_app = Flask(__name__)
db_control = SQLAlchemy(app)
sc_session = scoped_session(sessionmaker(bind=db_control.engine))


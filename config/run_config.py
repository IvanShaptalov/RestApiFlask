from flask import Flask
from config import config

print('run config')
app = Flask(__name__)
# database
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
# security
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

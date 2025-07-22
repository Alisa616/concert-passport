import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'Alisa'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/concert_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'Alisa'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/concert_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')

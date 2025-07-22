from flask_login import LoginManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from .models import Users
        return Users.query.get(int(user_id))

    from .routes import init_routes
    init_routes(app)

    with app.app_context():
        from . import models
        db.create_all()

    return app
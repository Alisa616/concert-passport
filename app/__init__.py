from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    from .routes import init_routes
    init_routes(app)

    with app.app_context():
        from . import models
        db.create_all()

    return app
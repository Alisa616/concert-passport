import os
import shutil
import tempfile
import pytest
from flask import Flask

from app import db
from app.routes import init_routes
from app.models import Users

@pytest.fixture(scope='session')
def _tmp_upload_dir():
    d = tempfile.mkdtemp(prefix="uploads_")
    yield d
    shutil.rmtree(d, ignore_errors=True)

@pytest.fixture
def app(_tmp_upload_dir):
    app = Flask(__name__)
    app.config.update(
        TESTING=True,
        SECRET_KEY='test-secret',
        SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_FOLDER=_tmp_upload_dir,
        ALLOWED_EXTENSIONS={'png', 'jpg', 'jpeg', 'gif'},
    )

    db.init_app(app)

    with app.app_context():
        db.create_all()

    init_routes(app)

    yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def ctx(app):
    with app.app_context():
        yield

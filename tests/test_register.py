from urllib.parse import urlparse

from app.models import Users
from app import db


def _pop_flashes(client):
    """Достаем флаш-сооб из сессии после запроса"""
    with client.session_transaction() as sess:
        flashes = sess.get('_flashes', [])
        sess['_flashes'] = []
    return flashes


def test_register_short_password_only(client):
    """Только короткий пароль(одна ошибка с паролем)"""
    resp = client.post(
        '/register',
        data={"name": "test_name_user", "email": "a@b.c", "password": "123"},
        follow_redirects=True
    )
    assert resp.status_code == 302
    flashes = _pop_flashes(client)
    assert flashes and flashes[0][0] == "danger"
    assert "Пароль должен быть не короче 6 символов." in flashes[0][1]


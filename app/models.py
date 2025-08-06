# app/models.py
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
import enum
from . import db


class ConcertType(enum.Enum):
    """Типы концертных событий"""
    solo = 'solo'
    tour = 'tour'
    festival = 'festival'


class Users(db.Model, UserMixin):
    """Модель пользователя"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    city = db.Column(db.String(100), nullable=True)
    birth_date = db.Column(db.Date, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    registered_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)

    # Связи
    attendance = db.relationship('Attendance', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        """Устанавливает хеш пароля"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Проверяет пароль"""
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def authenticate(email, password):
        """Аутентификация пользователя"""
        user = Users.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return user
        return None

    @property
    def age(self):
        """Возвращает возраст пользователя"""
        if self.birth_date:
            today = datetime.now().date()
            return today.year - self.birth_date.year - (
                        (today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None

    def __repr__(self):
        return f'<User {self.name} ({self.email})>'


class Artists(db.Model):
    """Модель артиста"""
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=True)

    # Связи
    concerts = db.relationship('Concerts', backref='artist', lazy=True, cascade='all, delete-orphan')

    @property
    def concerts_count(self):
        """Количество концертов артиста"""
        return len(self.concerts)

    def __repr__(self):
        return f'<Artist {self.name} ({self.genre})>'


class Concerts(db.Model):
    """Модель концерта"""
    __tablename__ = 'concerts'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    venue = db.Column(db.String(150), nullable=True)
    event_type = db.Column(db.Enum(ConcertType), nullable=False, default=ConcertType.solo)

    # Связи
    attendance = db.relationship('Attendance', backref='concert', lazy=True, cascade='all, delete-orphan')

    @property
    def is_upcoming(self):
        """Проверяет, предстоит ли концерт"""
        return self.event_date >= datetime.now().date()

    @property
    def attendees_count(self):
        """Количество посетителей"""
        return len(self.attendance)

    def __repr__(self):
        return f'<Concert: {self.artist.name} in {self.city} on {self.event_date}>'


class Attendance(db.Model):
    """Модель посещения концерта"""
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    concert_id = db.Column(db.Integer, db.ForeignKey('concerts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=True)  # Оценка от 1 до 5
    review = db.Column(db.Text, nullable=True)
    photo_url = db.Column(db.String(255), nullable=True)
    attended_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)

    # Ограничение уникальности: один пользователь может отметить посещение концерта только один раз
    __table_args__ = (db.UniqueConstraint('concert_id', 'user_id', name='unique_concert_user'),)

    def __repr__(self):
        return f'<Attendance: {self.user.name} at concert {self.concert_id}>'
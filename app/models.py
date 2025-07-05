from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import enum
from . import db

class ConcertType(enum.Enum):
    solo = 'solo'
    tour = 'tour'
    festival = 'festival'


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    city = db.Column(db.String(100), nullable=True)
    birth_date = db.Column(db.Date, nullable=True)
    registred_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)


    attendance = db.relationship('Attendance', backref='user', lazy=True)

    def __repr__(self):
        return '<Users %r>' % self.name

class Artists(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=True)

    concerts = db.relationship('Concerts', backref='artist', lazy=True)

    def __repr__(self):
        return '<Artists %r>' % self.name

class Concerts(db.Model):
    __tablename__ = 'concerts'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    venue = db.Column(db.String(150), nullable=True)
    event_type = db.Column(db.Enum(ConcertType), nullable=False, default=ConcertType.solo)

    attendance = db.relationship('Attendance', backref='concert', lazy=True)

    def __repr__(self):
        return f'<Concerts by {self.artist.name} in {self.city} on {self.event_date}>'

class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    concert_id = db.Column(db.Integer, db.ForeignKey('concerts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    review = db.Column(db.Text, nullable=True)
    photo_url = db.Column(db.String(255), nullable=True)
    attended_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Attendance by {self.user.name} for concert {self.concert_id}>'
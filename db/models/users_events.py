import hashlib

from db.core import db
from db.models.base import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    faculty = db.Column(db.String(50), nullable=False)
    is_blocked = db.Column(db.Boolean, default=False)

    @classmethod
    async def check_password(cls, password):
        password = await User.query.where(
            User.password == hashlib.md5(password.encode("utf-8")).hexdigest()).gino.first()
        return bool(password)

    @classmethod
    async def user_data(cls, password):
        usr = await User.select('name', 'faculty').\
            where(User.password == hashlib.md5(password.encode("utf-8")).hexdigest()).gino.first()
        return usr


class Event(TimedBaseModel):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)

    event_name = db.Column(db.String(50))
    user = db.Column(db.Integer, db.ForeignKey('users.id'))


class Photos(TimedBaseModel):
    __tablename__ = 'photos'

    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)

    event = db.Column(db.Integer, db.ForeignKey('events.id'))
    photo_path = db.Column(db.String(255))

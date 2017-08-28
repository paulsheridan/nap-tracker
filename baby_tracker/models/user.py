import bcrypt

import datetime
from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    DateTime,
    LargeBinary,
)

from sqlalchemy.orm import relationship
from .meta import Base, load_datetime


class User(Base):
    """User Class"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(Unicode(255), unique=True, nullable=False)
    password = Column(LargeBinary, nullable=False)
    last_logged = Column(DateTime, default=datetime.datetime.utcnow)

    meals = relationship('Meal', backref='user', lazy='dynamic')
    naps = relationship('Nap', backref='user', lazy='dynamic')

    def hash_password(self, pw):
        self.password = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
        return self.password.decode('utf8')

    def check_password(self, pw):
        expected_hash = self.password
        return bcrypt.checkpw(pw.encode('utf8'), expected_hash)

    @classmethod
    def from_json(cls, data):
        return cls(**{k:v for k, v in data.items() if k in {'email'}})

    def to_json(self):
        to_serialize = ['id', 'email']
        d = {}
        for attr_name in to_serialize:
            if isinstance(getattr(self, attr_name), datetime.datetime):
                d[attr_name] = getattr(self, attr_name).__str__()
            else:
                d[attr_name] = getattr(self, attr_name)
        return d

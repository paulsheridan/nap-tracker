import random
import string
import datetime
import bcrypt

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
    reset_secret = Column(Unicode(255))
    reset_expire = Column(DateTime)
    last_logged = Column(DateTime, default=datetime.datetime.utcnow)

    meals = relationship('Meal', backref='user', lazy='dynamic')
    naps = relationship('Nap', backref='user', lazy='dynamic')

    def hash_password(self, pw):
        if not validate_password(pw):
            raise ValueError
        self.password = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
        return self.password.decode('utf8')

    def check_password(self, pw):
        expected_hash = self.password
        return bcrypt.checkpw(pw.encode('utf8'), expected_hash)

    def generate_secret(self):
        self.reset_secret = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(16))
        self.reset_expire = datetime.datetime.now() + datetime.timedelta(days=3)
        return self.reset_secret

    def clear_secret(self):
        self.reset_secret = ''
        return self.reset_secret

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


def validate_password(pw):
    if len(pw) < 6 or ' ' in pw:
        return False
    return True

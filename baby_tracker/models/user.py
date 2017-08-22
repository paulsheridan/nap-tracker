from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    DateTime,
)

from sqlalchemy.orm import relationship
from .meta import Base, load_datetime


class User(Base):
    """User Class"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(Unicode(255), unique=True, nullable=False)
    password = Column(Unicode(255), nullable=False)
    last_logged = Column(DateTime, default=datetime.utcnow)

    meals = relationship('Meal', backref='user')
    naps = relationship('Nap', backref='user')

    @classmethod
    def from_json(cls, data):
        return cls(**{k:load_datetime(v) for k, v in data.items()})

    def to_json(self):
        to_serialize = ['id', 'email']
        d = {}
        for attr_name in to_serialize:
            if isinstance(getattr(self, attr_name), datetime):
                d[attr_name] = getattr(self, attr_name).__str__()
            else:
                d[attr_name] = getattr(self, attr_name)
        return d

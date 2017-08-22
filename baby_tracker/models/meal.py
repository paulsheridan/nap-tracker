from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Text,
    ForeignKey
)

from sqlalchemy.orm import relationship
from .meta import Base, load_datetime


class Meal(Base):
    __tablename__ = 'meals'
    id = Column(Integer, primary_key=True)
    time = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))

    @classmethod
    def from_json(cls, data):
        return cls(**{k:load_datetime(v) for k, v in data.items()})

    def to_json(self):
        to_serialize = ['id', 'time']
        d = {}
        for attr_name in to_serialize:
            if isinstance(getattr(self, attr_name), datetime):
                d[attr_name] = getattr(self, attr_name).__str__()
            else:
                d[attr_name] = getattr(self, attr_name)
        return d

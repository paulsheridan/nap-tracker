from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship
from .meta import Base, load_datetime
from .user import User


class Nap(Base):
    __tablename__ = 'naps'
    id = Column(Integer, primary_key=True)
    start = Column(DateTime, default=datetime.utcnow)
    end = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    @classmethod
    def from_json(cls, data):
        return cls(**{k:load_datetime(v) for k, v in data.items()})

    def to_json(self):
        to_serialize = ['id', 'start', 'end']
        nap_dict = {}
        for attr_name in to_serialize:
            if isinstance(getattr(self, attr_name), datetime):
                nap_dict[attr_name] = getattr(self, attr_name).__str__() + ' UTC'
            else:
                nap_dict[attr_name] = getattr(self, attr_name)
        return nap_dict

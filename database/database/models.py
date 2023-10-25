from typing import Any
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.types import Boolean
Base = declarative_base()


def to_dict(obj: Base) -> dict[str, Any]:
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


class Month(Base):
    __tablename__ = "months"
    player_name = Column("player_name", String, primary_key=True, nullable=False, unique=True)
    dates = Column("dates", String, nullable=False, unique=False)

class Player(Base):
    __tablename__ = "player"
    player_name = Column("player_name", String, primary_key=True, nullable=False, unique=True)
    name = Column('name', String, nullable=True)
    url = Column('url', String, nullable=True)
    title = Column('title', String, nullable=True)
    avatar = Column('avatar', String, nullable=True)
    player_id = Column('player_id', Integer, nullable=True)
    followers = Column('followers', Integer,nullable=True)
    country = Column('country', String, nullable=True)
    location = Column('location', String, nullable=True)
    joined = Column('joined', Integer, nullable=True)
    status = Column('status', String, nullable=True)
    is_streamer = Column('is_streamer', Boolean, nullable=True)
    twitch_url = Column('twitch_url', String, nullable=True)
    verified = Column('verified', Boolean, nullable=True)
    league = Column('league', String, nullable=True)
    
class Game(Base):
    __tablename__ = 'game'
    id = Column('id',Integer, primary_key = True)
    white = Column('white',String, nullable=False)
    black = Column('black',String, nullable=False)

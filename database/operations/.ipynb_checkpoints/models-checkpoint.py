from pydantic import BaseModel
from typing import Optional

class MonthCreateData(BaseModel):
    player_name: str
    dates: str
class MonthResult(BaseModel):
    player_name: str
    dates: str
class PlayerCreateData(BaseModel):
    player_name: str
    name: str = 'None'
    url: str = 'None'
    title: str = 'None'
    avatar: str = 'None'
    player_id: int = 0
    followers: int = 0
    country: str = 'None'
    location: str = 'None'
    joined: int = 0
    status: str = 'None'
    is_streamer: bool = False
    twitch_url: str = 'None'
    verified: bool = False
    league: str = 'None'

class PlayerResult(BaseModel):
    player_name: str
    name: str
    url: str
    title: str
    avatar: str
    player_id: int  
    followers: int
    country: str
    location: str
    joined: int
    status: str
    is_streamer: bool
    twitch_url: str
    verified: bool
    league: str
class GameCreateData(BaseModel):
    id: int
    black: str
    white: str
class GameResult(BaseModel):
    id: int
    black: str
    white: str
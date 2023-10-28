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
    start_time: str
    year: int
    month:int
    day:int
    white:str
    black:str
    white_elo:str
    black_elo:str
    white_result:str
    black_result:str
    time_control:str
    eco:str
    time_elapsed:str
    termination:str
    n_moves:str
class GameResult(BaseModel):
    id: int
    start_time: str
    year: int
    month:int
    day:int
    white:str
    black:str
    white_elo:str
    black_elo:str
    white_result:str
    black_result:str
    time_control:str
    eco:str
    time_elapsed:str
    termination:str
    n_moves:str
class MoveCreateData(BaseModel):
    id: int
    moves: str
    white_moves:str
    black_moves:str
    white_reaction_times:str
    black_reaction_times:str
    white_time_left:str
    black_time_left:str

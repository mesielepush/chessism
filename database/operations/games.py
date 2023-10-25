#from .utils.ask_db import player_exists_at_db
#from .chess_com_api import get_profile
from .interface import DataInterface
from .models import GameCreateData, GameResult
from fastapi.responses import PlainTextResponse
from .date_format import create_range, just_new_dates
from .download_games import download_months
from .games_format import insert_games
from datetime import datetime 
import joblib
from database.database.db_interface import DBInterface
from database.database.models import Player, Game, Month
player_interface = DBInterface(Player)

def html_response(content):
    return PlainTextResponse(content=content, status_code=200)


def read_all_games(games_interface: DataInterface) -> list[GameResult]:
    games = games_interface.read_all()
    return [GameResult(**p) for p in games]


def read_game(game_id: int, games_interface: DataInterface) -> GameResult:
    game = games_interface.read_by_id(game_id)
    return GameResult(**game)


def create_game(
    data: dict, games_interface: DataInterface) -> GameResult:
    data['white'] = data['white'].lower()
    data['black'] = data['black'].lower()
    game = games_interface.create(GameCreateData(**data).model_dump())
    return GameResult(**game)
    
def create_games(data: dict) -> str:
    date_range = create_range(data)
    if type(date_range) == str:
        return html_response(date_range)
    print(date_range)
    valid_range = just_new_dates(data['player_name'], date_range)
    games = download_months(data['player_name'],valid_range)
    games = insert_games(data['player_name'], games)
    print('gamespkl')
    joblib.dump(games, 'games.pkl')
    print('games_pkl')
    print('###########################')
    print(games)
    print('###########################')
    return html_response('DONEEEEEEEEEEE')






    
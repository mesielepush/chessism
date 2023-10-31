import multiprocessing as mp
from database.database.models import Game
from .format_dates import create_range
from .format_games import insert_games
from fastapi.encoders import jsonable_encoder
from fastapi.responses import PlainTextResponse, JSONResponse
from .models import GameCreateData
from database.database.db_interface import DBInterface
from .chess_com_api import download_months
import joblib
game_interface = DBInterface(Game)
def html_response(content):
    return PlainTextResponse(content=content, status_code=200)

def read_game(data):
    player = data
    player = jsonable_encoder(player)
    return JSONResponse(content=player)
    
def create_games(data:dict)->str:
    date_range = create_range(data)
    if type(date_range) == str:
        return html_response(date_range)
    print(date_range)
    valid_range = date_range
    #valid_range = just_new_dates(data['player_name'], date_range)
    games = download_months(data['player_name'],valid_range)
    joblib.dump(games, 'games.pkl')
    games = insert_games(data['player_name'], games, valid_range)
    # player = jsonable_encoder(date_range)
    # return JSONResponse(content=date_range)
    return html_response('Games_done')
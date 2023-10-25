#from .utils.ask_db import player_exists_at_db
from .chess_com_api import get_profile
from .interface import DataInterface
from .models import PlayerCreateData, PlayerResult
from fastapi.responses import PlainTextResponse


def html_response(content):
    return PlainTextResponse(content=content, status_code=200)

def read_all_players(players_interface: DataInterface) -> list[PlayerResult]:
    players = players_interface.read_all()
    return [PlayerResult(**p) for p in players]

def read_player(player_id: int, players_interface: DataInterface) -> PlayerResult:
    player = players_interface.read_by_id(player_id)
    return PlayerResult(**player)
def create_player(
    data: dict, player_interface: DataInterface) -> PlayerResult:
    if player_interface.player_exists(data['player_name'].lower()):
         return html_response("player already exists at DB")
    profile = get_profile(data['player_name'])
    if not profile:
        return html_response("player_name doesn't exists at chess.com")
    if type(profile) == str:
        raise Exception(profile)
    profile['player_name'] = data['player_name'].lower()
    player = player_interface.create(PlayerCreateData(**profile).model_dump())
    return PlayerResult(**player)
def read_oponents(data: dict, player_interface: DataInterface) -> list:
    return player_interface.read_oponents(data['player_name'])
    
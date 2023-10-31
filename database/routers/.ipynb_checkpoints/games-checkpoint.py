from fastapi import APIRouter
from database.database.db_interface import DBInterface
from database.database.models import Game, Player, Month
from database.operations.games import (
    create_game,
    read_all_games,
    read_game,
    create_games
)
from database.operations.models import (
    GameCreateData,
    GameResult,
)

router = APIRouter()


@router.get("/games")
def api_read_all_games() -> list[GameResult]:
    game_interface = DBInterface(Game)
    return read_all_games(game_interface)


@router.get("/games/{game_id}")
def api_read_game(game_id: int) -> GameResult:
    game_interface = DBInterface(Game)
    return read_game(game_id, game_interface)


@router.post("/game")
def api_create_game(game: dict) -> GameResult:
    game_interface = DBInterface(Game)
    return create_game(game, game_interface)
@router.post("/games")
def api_create_games(data: dict) -> str:
    player_interface = DBInterface(Player)
    game_interface = DBInterface(Game)
    month_interface = DBInterface(Month)
    return create_games(data)
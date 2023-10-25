from fastapi import APIRouter
from database.database.db_interface import DBInterface
from database.database.models import Player
from database.operations.players import (
    create_player,
    read_all_players,
    read_player,
)
from database.operations.models import (
    PlayerCreateData,
    PlayerResult,
)

router = APIRouter()


@router.get("/players")
def api_read_all_players() -> list[PlayerResult]:
    player_interface = DBInterface(Player)
    return read_all_players(player_interface)


@router.get("/players/{players_id}")
def api_read_players(player_id: int) -> PlayerResult:
    player_interface = DBInterface(Player)
    print(player_id)
    return read_player(player_id, player_interface)


@router.post("/player")
def api_create_player(player: dict) -> PlayerResult:
    player_interface = DBInterface(Player)
    return create_player(player, player_interface)
import numpy as np
from .chess_com_api import get_profile
from .models import PlayerCreateData
import concurrent
import os
import psycopg2
import multiprocessing as mp
from database.database.db_interface import DBInterface
from database.database.models import Player, Game, Month

def get_ask_connection():
    CONN_STRING = os.getenv("PSYCOPG2_CONN_STRING")
    return psycopg2.connect(CONN_STRING, port = 5433)
def player_exists_at_db(player_name: str):
    conn = get_ask_connection()
    with conn.cursor() as curs:
        curs.execute(
            f"select player_name from player where player_name='{player_name}'"
        )
        result = curs.fetchall()
    if len(result) == 1:
        return True
    return False
def open_request(sql_question:str):
    conn = get_ask_connection()
    with conn.cursor() as curs:
        curs.execute(
            sql_question
        )
        result = curs.fetchall()
    return result
player_interface = DBInterface(Player)
game_interface = DBInterface(Game)
month_interface = DBInterface(Month)
def get_new_links(new_links):
    # new = []
    # for id_ in new_links:

    #     if len(open_request(f"select id from game where game.id == {id_}"))
    # open_request(f"select id from game where game.id == ")
def get_player_profile(params):
    player_name = params['player_name']    
    profile = {'player_name':player_name}
    profile = PlayerCreateData(**profile)
    params['profiles'].append(profile.model_dump())
def insert_players(new_players):
    print('II')
    profiles = mp.Manager().list()
    params = [
                {
                    "player_name": player_name,
                    "profiles": profiles,
                }
                for player_name in new_players
            ]
 
    print("Entering Pooling")
    pool = mp.Pool(3, maxtasksperchild=1)
    with pool:
        pool.map(get_player_profile, params)
    print("Out of the Pool")
    print(profiles)
    if len(list(profiles)) == 0:
        return []
    return list(profiles)

def insert_new_players(new_players):
    new = []
    for player in new_players:
        if player_exists_at_db(player):
            continue
        else:
            new.append(player)
    if len(new)==0:
        print('ZERO NEW PLAYERS')
        return
    profiles = insert_players(new)
    print('len players',len(profiles))
    player_interface.create_all(profiles)
    print(f'{len(profiles)} NEW PLAYERS')
    return

# def get_new_players(player_name,players_this_month):
#     all_players = set(player_interface.read_all())
#     players_this_month = set(players_this_month)
#     new_players = list(players_this_month - all_players)
#     new_players = [player for player in new_players if len(player)!=0]
#     print('#########################')
#     print('new_players', len(new_players))
#     print('#########################')
#     return new_players

def get_pgn_item(game, item: str) -> str:
    if item == "Termination":
        return (
            game.split(f"{item}")[1]
            .split("\n")[0]
            .replace('"', "")
            .replace("]", "")
            .lower()
        )
    return (
        game.split(f"{item}")[1]
        .split("\n")[0]
        .replace('"', "")
        .replace("]", "")
        .replace(" ", "")
        .lower()
    )

def clean_games(game: str) -> bool:
    """
    It validates games for length of moves and formatting errors

    """
    game_with_more_than_n_moves = "10. "  # format: 'INT. '

    try:
        game.split("\n\n")[1][:-4]
    except:
        return False
    if not game_with_more_than_n_moves in game.split("\n\n")[1][:-4]:
        return False
    if game.split("\n\n")[1][:-4].startswith("1... "):
        return False
    if (
        "/"
        in game.split(f"TimeControl")[1]
        .split("\n")[0]
        .replace('"', "")
        .replace("]", "")
        .replace(" ", "")
        .lower()
    ):
        return False
    return True
def validate_games(player_name, games):
    
    print(f"GAMES BEFORE CLEANING = {len(games)}")
    games = [game for game in games if clean_games(game)]
    print(f"GAMES AFTER CLEANING = {len(games)}")

    players_and_game_id = np.array(
        [
            [
                get_pgn_item(game, "White").lower(),
                get_pgn_item(game, "Black").lower(),
                int(get_pgn_item(game, "[Link").split("/")[-1]),
            ]
            for game in games
        ]
    )

    players_this_month = set(players_and_game_id[:, 0])
    black_players_this_month = set(players_and_game_id[:, 1])
    players_this_month.update(black_players_this_month)
    insert_new_players(players_this_month)
    new_links = get_new_links(players_and_game_id[:, 2])
    
    # valid_games = get_valid_links(
    #     player_name, games, links_this_month, players_this_month
    # )

    # if len(valid_games) == 0:
    #     return False
    return 'DONME'
def insert_games(player_name, games):
    valid_games = validate_games(player_name, games)
    return valid_games

    
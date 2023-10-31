import numpy as np
from .chess_com_api import get_profile
from .models import PlayerCreateData
import concurrent
import multiprocessing as mp
from database.database.db_interface import DBInterface
from database.database.models import Player, Game, Month
player_interface = DBInterface(Player)
game_interface = DBInterface(Game)
month_interface = DBInterface(Month)
def get_new_links(new_links):
    ...
def insert_player(params):
    player_name = params['player_name']
    if player_interface.player_exists(player_name):
         return
    profile = {'player_name':player_name}
    profile = PlayerCreateData(**profile)
    params['profiles'].append(profile)
    
def get_new_profiles(new_players):
    # profiles = []
    # if not player_interface.player_exists(player_name):
    #      new_players.append(player_name)
    # for new_player in new_players:
    #     profile = get_profile(new_player)
    #     if type(profile) == str:
    #         print('777777777777777777')
    #         print(profile, new_player)
    #         print('777777777777777777')           
    #     profile['player_name'] = new_player
    #     profile = PlayerCreateData(**profile)
    #     profiles.append(profile)
    # return [profile.model_dump() for profile in profiles]
    # profiles = []
    # params = [
    #     {
    #         "player_name": player_name,
    #         "profiles": profiles,
    #     }
    #     for player_name in new_players
    # ]
    # print(params)
    # with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
    #     executor.map(insert_player, params)
    profiles = mp.Manager().list()
    params = [
                {
                    "player_name": player_name,
                    "profiles": profiles,
                }
                for player_name in new_players
            ]

    print("Entering Pooling")
    pool = mp.Pool(6)
    with pool:
        pool.map(insert_player, params)
    print("Out of the Pool")
    return list(profiles)

def insert_new_players(new_players):
    print('insert begin')
    profiles = get_new_profiles(new_players)
    player_interface.create_all(profiles)
    return profiles

def get_new_players(player_name,players_this_month):
    all_players = set(player_interface.read_all())
    players_this_month = set(players_this_month)
    new_players = list(players_this_month - all_players)
    new_players = [player for player in new_players if len(player)!=0]
    print('#########################')
    print('new_players', len(new_players))
    print('#########################')
    return new_players

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
    """
    It gets the names of every player in the new games
    it gets the links of every game played before with the new players
    it inserts new players to the db
    it drops game_links already at db
    returns new games not in the db
    """
    print(f"GAMES BEFORE CLEANING = {len(games)}")
    # First the local constrains: more than 14 moves and formatting
    games = [game for game in games if clean_games(game)]
    # then to check all players in games and insert the new ones
    # then to check all if some of the games are already in the db and exclude them
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
    
    new_players = players_this_month #get_new_players(player_name, players_this_month)
    a = insert_new_players(new_players)
    # new_links = get_new_links(players_and_game_id[:, 2])
    
    # valid_games = get_valid_links(
    #     player_name, games, links_this_month, players_this_month
    # )

    # if len(valid_games) == 0:
    #     return False
    return a
def insert_games(player_name, games):
    valid_games = validate_games(player_name, games)
    return valid_games

    
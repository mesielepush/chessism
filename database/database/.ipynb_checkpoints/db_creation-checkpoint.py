import os
from dotenv import load_dotenv
import re
import concurrent.futures
import pandas as pd
import numpy as np
from .chess_com_api import download_month
from .validations import get_valid_dates

load_dotenv(".env")
N_THREADS = int(os.getenv("N_THREADS"))


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


def create_month(params: list) -> None:
    """
    ask chess com for the games of the month
    and it splits the games and appends separated games to an outside list.
    """
    pgn = download_month(params["player_name"], params["year"], params["month"])
    if pgn == False:
        params["return_games"].extend(False)
        return
    games = pgn.read().split("\n\n\n")
    params["return_games"].extend(games)


def get_games(player_name: str, date: str) -> list:
    """
    Validate if we already asked for those months in chessdotcom
    if not, then ask chessdotcom for data trough a threadpool
    returns valid games for valid months and a list of months asked
    """
    valid_dates = get_valid_dates(player_name, date)
    if len(valid_dates) == 0:
        return False, False
    print("valid dates", len(valid_dates))
    return_games = []
    params = [
        {
            "player_name": player_name,
            "year": date[0],
            "month": date[1],
            "return_games": return_games,
        }
        for date in valid_dates
    ]

    print("entering concurrent")
    with concurrent.futures.ThreadPoolExecutor(max_workers=N_THREADS) as executor:
        executor.map(create_month, params)
    print(f"GOT {len(return_games)} games")
    print("downloading over")
    return_games = [game for game in return_games if game is not False]

    return return_games, valid_dates


def get_games_classes(params: dict) -> None:
    """
    Interface to load the result of making one game_class creation
    returns foreign list.append() from read_games: mp.Pool
    """
    game_dict, moves_data = create_game_dict(params[0])
    params[1].append(game_dict)
    params[2].append(moves_data)


def create_game_dict(game: str) -> tuple:
    """
    Self explanatory
    """
    link = int(get_pgn_item(game, "[Link").split("/")[-1])
    game_dict = dict()
    n_moves, moves_data = get_moves_data(game)
    game_dict["link"] = link
    game_dict["start_time"] = get_pgn_item(game, "StartTime")
    game_dict["year"] = int(get_pgn_item(game, "Date")[:4])
    game_dict["month"] = int(get_pgn_item(game, "Date")[5:7])
    game_dict["day"] = int(get_pgn_item(game, "Date")[8:10])
    game_dict["white"] = get_pgn_item(game, "White").lower()
    game_dict["black"] = get_pgn_item(game, "Black").lower()
    game_dict["white_elo"] = get_pgn_item(game, "WhiteElo")
    game_dict["black_elo"] = get_pgn_item(game, "BlackElo")
    game_dict["white_result"] = get_result(
        get_pgn_item(game, "White").lower(), get_pgn_item(game, "Termination")
    )
    game_dict["black_result"] = get_result(
        get_pgn_item(game, "Black").lower(), get_pgn_item(game, "Termination")
    )
    game_dict["time_control"] = get_pgn_item(game, "TimeControl")
    game_dict["eco"] = get_eco(game)
    game_dict["time_elapsed"] = get_time_elapsed(game)
    game_dict["termination"] = clean_termination(get_pgn_item(game, "Termination"))
    game_dict["n_moves"] = n_moves

    moves_data["link"] = link
    return game_dict, moves_data


def get_moves_data(game: str) -> tuple:
    """
    calculates n_moves
    It separates the white and black moves,
    claculates reaction times for both players
    returns a dictionary with keys:
                        moves:["1...n_moves"],
                        moves_white["e4..."], moves_black["e5..."],
                        white_reaction_times["0.1,0.5,1..."], black_reaction_times["0.1,0.2,0.1..."]
                        white_time_left["59.9,59.4,58.4"], black_time_left["59.9,59.7,59.6"]

    """
    time_bonus = get_time_bonus(game)
    raw_moves = (
        game.split("\n\n")[1]
        .replace("1/2-1/2", "")
        .replace("1-0", "")
        .replace("0-1", "")
    )
    n_moves = get_n_moves(raw_moves)
    times = [x.replace("]", "").replace("}", "") for x in raw_moves.split() if ":" in x]
    no_times = re.sub(r"{[^}]*}*", "", raw_moves)
    clean_moves = [x for x in no_times.split() if "." not in x]
    if not f"{n_moves}..." in raw_moves:
        clean_moves.append("-")
        times.append("-")
    moves_data = create_moves_table(times, clean_moves, n_moves, time_bonus)
    return n_moves, moves_data


def get_result(user_name, result):
    if "drawn" in result:
        return 0.5
    if user_name in result:
        return 1
    else:
        return 0


def get_time_elapsed(game):
    start = get_pgn_item(game, "Date") + " " + get_pgn_item(game, "StartTime")
    end = get_pgn_item(game, "EndDate") + " " + get_pgn_item(game, "EndTime")
    delta = pd.to_datetime(end) - pd.to_datetime(start)
    return str(delta).split()[-1]


def clean_termination(one_termination: str):
    if "drawn" in one_termination:
        return one_termination.replace("game drawn by ", "")
    if "time" in one_termination:
        return "time"
    if "abandoned" in one_termination:
        return "abandoned"
    if "checkmate" in one_termination:
        return "checkmate"
    if "resignation" in one_termination:
        return "resignation"
    return one_termination


def get_eco(game: str):
    try:
        return get_pgn_item(game, "ECO")
    except:
        return "no_eco"


def get_time_bonus(game):
    time_control = get_pgn_item(game, "TimeControl")
    if "+" in time_control:
        return int(time_control.split("+")[-1])
    return 0


def get_n_moves(raw_moves):
    return max(
        [
            int(x.replace(".", ""))
            for x in raw_moves.split()
            if x.replace(".", "").isnumeric()
        ]
    )


def create_moves_table(
    times: list, clean_moves: list, n_moves: int, time_bonus: int
) -> dict[str]:
    """
    it transfor the row moves and times_left into two columns
    it assing the moves to white and black
    calculates the times_left to get reaction times
    it return a dict with a single string
    """
    ordered_times = np.array(times).reshape((-1, 2))
    ordered_moves = np.array(clean_moves).reshape((-1, 2))
    white_times = pd.Series(
        [
            pd.Timedelta(str(str_time)).total_seconds()
            for str_time in ordered_times[:, 0]
        ]
    )
    black_times = pd.Series(
        [
            pd.Timedelta(str(str_time)).total_seconds()
            for str_time in ordered_times[:, 1]
            if str_time != "-"
        ]
    )
    white_cumsub = white_times.sub(white_times.shift(-1)) + time_bonus
    black_cumsub = black_times.sub(black_times.shift(-1)) + time_bonus

    result = {
        "moves": "".join([str(x) + " " for x in range(1, n_moves + 1)])[:-1],
        "white_moves": "".join([str(x) + " " for x in ordered_moves[:, 0]])[:-1],
        "white_reaction_times": "".join([str(x) + " " for x in white_cumsub])[:-1],
        "white_time_left": "".join([str(x) + " " for x in white_times])[:-1],
        "black_moves": "".join([str(x) + " " for x in ordered_moves[:, 1]])[:-1],
        "black_reaction_times": "".join([str(x) + " " for x in black_cumsub])[:-1],
        "black_time_left": "".join([str(x) + " " for x in black_times])[:-1],
    }
    return result

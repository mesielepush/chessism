import os
from dotenv import load_dotenv
import requests
import json
import io

load_dotenv(".env")


def member_exists(player_name: str):
    """It ask for the chessdotcom profile
    returns a boolean indicating the existence of the player
    """
    PLAYER = os.getenv("PLAYER").replace("{player_name}", player_name)
    request = requests.get(PLAYER, timeout=3)
    request = request.__dict__["_content"].decode("utf-8")
    response = json.loads(request)

    if "message" in response:
        return False
    return True


def ask_twice(player_name: str, year: int, month: int):
    import time

    DOWNLOAD_MONTH = (
        os.getenv("DOWNLOAD_MONTH")
        .replace("{player_name}", player_name)
        .replace("{year}", str(year))
        .replace("{month}", str(month))
    )
    games = requests.get(DOWNLOAD_MONTH, allow_redirects=True, timeout=10)
    if len(games.content) == 0:
        time.sleep(1)
        games = requests.get(DOWNLOAD_MONTH, allow_redirects=True, timeout=10)
    if len(games.content) == 0:
        return False
    return games


def download_month(player_name: str, year: int, month: int) -> str:
    """It ask for a month of games of a particular player
    the games package is a pgn_txt.
    Returns:
        io.str
    """
    games = ask_twice(player_name, year, month)
    pgn = io.StringIO(games.content.decode().replace("'", '"'))
    return pgn


def get_member_since(player_name):
    """It ask for the chessdotcom profile
    returns the date of creation of the account
    """
    PLAYER = os.getenv("PLAYER").replace("{player_name}", player_name)
    request = requests.get(PLAYER, timeout=3)
    request = request.__dict__["_content"].decode("utf-8")
    return json.loads(request)["joined"]
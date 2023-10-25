import os
from dotenv import load_dotenv
import requests
import json
import io
import time

load_dotenv(".env")
def get_profile(player_name):
    PLAYER = os.getenv("PLAYER").replace("{player_name}", player_name.lower())
    USER_AGENT = os.getenv('USER_AGENT')
    response = requests.get(PLAYER, timeout=3, headers = {"User-Agent": USER_AGENT})
    time.sleep(1)
    if response.status_code == 200:
        response = response.__dict__["_content"].decode("utf-8")
        response = json.loads(response)
        response.pop('@id')
        response.pop('username')
        response.pop('last_online')
        country = response.pop('country').split('/')[-1]
        response['country'] = country
        if "message" in response:
            return False
        return response
    else:
        return f'RESPONSE {response.status_code}'

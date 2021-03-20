# Using https://github.com/Henrik-3/unofficial-valorant-api
import requests
from requests.exceptions import HTTPError
import json
from datetime import datetime, timezone

base = "https://api.henrikdev.xyz"

def get_player_list():
    with open('player_list.txt') as f:
        player_list = list(f)
        player_list = [x.rstrip() for x in player_list]
        return player_list

def add_player_to_list(player: str):
    with open('player_list.txt', 'r+') as f:
        for line in f:
            if player == line[:-1]:
                return "Player already in database (txt file lol [like the UK governement uses])."
                break
        else:
            f.write(f"{player}\n")
            return "Done."

def remove_player_from_list(player: str):
    with open("player_list.txt", "r+") as f:
        d = f.readlines()
        if player+"\n" not in d:
            return "Player not in database"
        f.seek(0)
        for i in d:
            if i.strip('\n') != player:
                f.write(i)
        f.truncate()
    return "Done."


def get_match_info(player):
    try:
        name, tag = player.split('#')
    except ValueError:
        return None
    url = f"{base}/valorant/v3/matches/eu/{name}/{tag}"
    try:
        response = requests.get(url)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
        return "ERROR: Too many requests."
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    return response

def check_last_online(player):
    try:
        response = get_match_info(player).json()
    except AttributeError:
        return "ERROR: Too many requests."
    with open('tmp.txt', 'r+') as f: 
        metadata = response['data']['matchres'][0]['metadata']
        game_start, game_length = metadata['game_start'], metadata['game_length']
        game_end = (game_start + game_length)/1000
        return datetime.fromtimestamp(game_end, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

def check_last_onlines():
    return [f"{player}|{check_last_online(player)}" for player in get_player_list()]

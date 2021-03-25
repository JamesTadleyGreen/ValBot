# Using https://github.com/Henrik-3/unofficial-valorant-api
import requests
from requests.exceptions import HTTPError
import json
from datetime import datetime, timezone

base = "https://api.henrikdev.xyz"

def get_online(player):
    try:
        name, tag = player.split('#')
    except ValueError:
        return None
    url = f"{base}/valorant/v1/live-match/{name}/{tag}"
    response = requests.get(url)
    if response.status_code == 200:
        return True
    return False

def get_live_info(player):
    try:
        name, tag = player.split('#')
    except ValueError:
        return None
    url = f"{base}/valorant/v1/live-match/{name}/{tag}"
    response = requests.get(url)
    return response


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
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    return response

def get_player_info(player):
    try:
        name, tag = player.split('#')
    except ValueError:
        return None
    url = f"{base}/valorant/v2/mmr/eu/{name}/{tag}"
    try:
        response = requests.get(url)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    return response

def get_player_rank(player):
    name, tag = player.split('#')
    try:
        rank_data = get_player_info(player).json()
    except AttributeError:
        return None
    return rank_data['data']['current_data']

def check_last_online(player):
    try:
        response = get_match_info(player).json()
    except json.decoder.JSONDecodeError:
        return None
    metadata = response['data']['matchres'][0]['metadata']
    game_start, game_length = metadata['game_start'], metadata['game_length']
    game_end = (game_start + game_length)/1000
    return datetime.fromtimestamp(game_end, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')



def DEV_output_to_file(func, file, player):
    with open(f"{file}.txt", "w") as f:
        f.write(json.dumps(func(player).json(), indent=4))


# FAILSAFE
# old_player_list = ["Chicken#80085", "KimJong#42069", "EpicVipa#EUW", "Chicken#7724", "DawnOfTheLiving#EUW"]
# for player in old_player_list:
#     add_player_to_list(player)
# print(update_players_info())

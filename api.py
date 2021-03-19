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
                print("Player already in database (txt file lol [like the UK governement does]).")
                break
        else:
            f.write(f"{player}\n")

def get_match_info(player):
    name, tag = player.split('#')
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

def check_last_online(player):
    response = get_match_info(player).json()
    with open('tmp.txt', 'r+') as f: 
        metadata = response['data']['matchres'][0]['metadata']
        game_start, game_length = metadata['game_start'], metadata['game_length']
        game_end = (game_start + game_length)/1000
        return datetime.fromtimestamp(game_end, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

def check_last_onlines():
    return [f"{player}: {check_last_online(player)}" for player in get_player_list()]



# #print(get_match_info('Chicken#7724').content)
# print(check_last_onlines())
# # 1616176949766
# # 2239902

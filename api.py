# Using https://github.com/Henrik-3/unofficial-valorant-api
import requests
from requests.exceptions import HTTPError
import json
from datetime import datetime, timezone

base = "https://api.henrikdev.xyz"

def get_player_list():
    with open('player_list.txt') as f:
        return json.load(f)

def add_player_to_list(player: str):
    name, tag = player.split('#')
    with open('player_list.txt', 'r+') as f:
        json_data = json.load(f) # {players: []}
        for player in json_data['players']:
            if player['name'] == name and player['tag'] == tag:
                return "Player already in database (txt file lol [like the UK governement uses])."
        else:
            json_data['players'].append({"name": name, "tag": tag, "nickname": f"{name}#{tag}", "rank_data": {}, "last_online": None})
            f.truncate(0)
            f.seek(0)
            f.write(json.dumps(json_data, indent=4))
            return "Done."   

def remove_player_from_list(player: str): #TODO fix
    name, tag = player.split('#')
    with open('player_list.txt', 'r+') as f:
        json_data = json.load(f) # {players: []}
        for player in json_data['players']:
            if player['name'] == name and player['tag'] == tag:
                json_data['players'].remove(player)
                f.truncate(0)
                f.seek(0)
                f.write(json.dumps(json_data, indent=4))
                return "Removed player."
        else:
            return "Player not found."

def set_player_nickname(player: str, nickname: str):
    name, tag = player.split('#')
    with open('player_list.txt', 'r+') as f:
        json_data = json.load(f) # {players: []}
        for player in json_data['players']:
            if player['name'] == name and player['tag'] == tag:
                player['nickname'] = nickname
                f.truncate(0)
                f.seek(0)
                f.write(json.dumps(json_data, indent=4))
                return "Done."
        else:
            return "Player not found."  


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
        return "ERROR: Too many requests."
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    return response

def get_player_rank(player):
    name, tag = player.split('#')
    try:
        rank_data = get_player_info(player).json()
    except AttributeError:
        return "ERROR: Too many requests."
    return rank_data['data']['current_data']

def rank_emoji(rank_num):
    rank, number = rank_num.split(" ")
    with open('emoji_lookup.txt', 'r+') as f:
        json_data = json.load(f)
        return json_data[rank]*int(number)

def rank_prog_emoji(prog_in_tier: int):
    if prog_in_tier == 0:
        return ":poop:"
    if prog_in_tier > 90:
        return ":100:"
    return ":green_heart:"*((prog_in_tier+5)//10) + ":black_heart:"*(10-(prog_in_tier+5)//10)

def update_players_info():
    print("Updating info")
    with open('player_list.txt', 'r+') as f:
        json_data = json.load(f)
        for player in json_data['players']:
            player_id = f"{player['name']}#{player['tag']}"
            try:
                player['rank_data'] = get_player_rank(player_id)
            except AttributeError:
                pass
            try:
                player['last_online'] = check_last_online(player_id)
            except AttributeError:
                pass
        f.truncate(0)
        f.seek(0)
        f.write(json.dumps(json_data, indent=4))
        return "Done."

def check_last_online(player):
    try:
        response = get_match_info(player).json()
    except AttributeError:
        return "ERROR: Too many requests."
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

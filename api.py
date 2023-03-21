# Using https://github.com/Henrik-3/unofficial-valorant-api
from typing import Tuple
import requests
from requests.exceptions import HTTPError
import json
from datetime import datetime, timezone

base = "https://api.henrikdev.xyz"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
}


def get_online(player):
    try:
        name, tag = player.split("#")
    except ValueError:
        return None
    url = f"{base}/valorant/v1/live-match/{name}/{tag}"
    response = requests.get(url)
    if response.status_code == 200:
        return True
    return False


def get_live_info(player):
    try:
        name, tag = player.split("#")
    except ValueError:
        return None
    url = f"{base}/valorant/v1/live-match/{name}/{tag}"
    response = requests.get(url, headers=headers)
    return response


def get_match_info(player):
    try:
        name, tag = player.split("#")
    except ValueError:
        return None
    url = f"{base}/valorant/v3/matches/eu/{name}/{tag}"
    try:
        response = requests.get(url, headers=headers)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Python 3.6
        return None
    except Exception as err:
        print(f"Other error occurred: {err}")  # Python 3.6
    return response


def get_player_info(player):
    try:
        name, tag = player.split("#")
    except ValueError:
        return None
    url = f"{base}/valorant/v2/mmr/eu/{name}/{tag}"
    try:
        response = requests.get(url, headers=headers)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Python 3.6
        return None
    except Exception as err:
        print(f"Other error occurred: {err}")  # Python 3.6
    return response


def get_player_rank(player):
    try:
        rank_data = get_player_info(player).json()
    except AttributeError:
        return None
    return rank_data["data"]["current_data"]


def check_last_online(player):
    try:
        response = get_match_info(player).json()
    except json.decoder.JSONDecodeError:
        return None
    metadata = response["data"][0]["metadata"]
    game_start, game_length = metadata["game_start"], metadata["game_length"]
    game_end = game_start + game_length / 1000
    return datetime.fromtimestamp(game_end, timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def DEV_output_to_file(func, file, player):
    with open(f"{file}.txt", "w") as f:
        f.write(json.dumps(func(player).json(), indent=4))


def graph_data(
    player_name: str, dependent: str, cum: bool, isolate: bool
) -> list[Tuple[list[float], list[float]]]:
    keys = dependent.split("/")
    match_info = get_match_info(player_name).json()["data"][0]
    output = {
        player["puuid"]: ([], []) for player in match_info["players"]["all_players"]
    }
    rounds = match_info["rounds"]
    for i, round in enumerate(rounds):
        player_stats = round["player_stats"]
        for player in player_stats:
            if isolate and player_name != player["player_display_name"]:
                continue
            player_id = player["player_puuid"]
            for key in keys:
                x = i
                y = (
                    player[key] + output[player_id][1][-1]
                    if (cum and len(output[player_id][1]) > 0)
                    else player[key]
                )
                output[player_id][0].append(x)
                output[player_id][1].append(y)
    return {
        [
            f'{player["name"]} - {player["character"]}'
            for player in match_info["players"]["all_players"]
            if player["puuid"] == pid
        ][0]: output[pid]
        for pid in output
    }


print(graph_data("CHICKEN#9771", "legshots", cum=True, isolate=True))

# FAILSAFE
# old_player_list = ["Chicken#80085", "KimJong#42069", "EpicVipa#EUW", "Chicken#7724", "DawnOfTheLiving#EUW"]
# for player in old_player_list:
#     add_player_to_list(player)
# print(update_players_info())

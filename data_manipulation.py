import json
import api


def get_player_list():
    with open("player_list.txt") as f:
        return json.load(f)


def rank_emoji(rank_num):
    rank, number = rank_num.split(" ")
    with open("emoji_lookup.txt", "r+") as f:
        json_data = json.load(f)
        return json_data[rank] * int(number)


def rank_prog_emoji(prog_in_tier: int):
    if prog_in_tier == 0:
        return ":poop:"
    if prog_in_tier > 90:
        return ":100:"
    return ":green_heart:" * ((prog_in_tier + 5) // 10) + ":black_heart:" * (
        10 - (prog_in_tier + 5) // 10
    )


def last_to_die(match):
    """Generates a score for pussyness and slow rotatingness

    Args:
        match (json): match data

    Returns:
        dict: values for the metrics described above
    """
    # Name Pussy_score Slow_rotate_score
    pussy_time = 1000 * 20
    rotate_time = pussy_time
    d = {"Red": [], "Blue": []}
    for player in match["players"]["red"]:
        d["Red"].append(
            {
                "name": player["name"] + "#" + player["tag"],
                "pussy_score": 0,
                "rotate_score": 0,
            }
        )
    for player in match["players"]["blue"]:
        d["Blue"].append(
            {
                "name": player["name"] + "#" + player["tag"],
                "pussy_score": 0,
                "rotate_score": 0,
            }
        )
    for i, round in enumerate(match["rounds"]):
        deaths = []
        if round["winning_team"] == "Red":
            losing_team = "Blue"
        elif round["winning_team"] == "Blue":
            losing_team = "Red"
        for player_stat in round["player_stats"]:
            for kill in player_stat["kill_events"]:
                for player in d[losing_team]:
                    if kill["victim_display_name"] in player["name"]:
                        deaths.append(
                            {
                                "time": kill["kill_time_in_round"],
                                "name": kill["victim_display_name"],
                            }
                        )
        deaths.sort(key=lambda d: d["time"])
        if len(deaths) >= len(d[losing_team]):
            for player in d[losing_team]:
                if player["name"] == deaths[-1]["name"]:
                    if (i <= 12 and losing_team == "Red") or (
                        i > 12 and losing_team == "Blue"
                    ):  # initial attack = Red
                        if deaths[-1]["time"] - deaths[-2]["time"] > pussy_time:
                            player["pussy_score"] += 1
                    else:
                        if deaths[-1]["time"] - deaths[-2]["time"] > rotate_time:
                            player["rotate_score"] += 1
        elif (
            len(deaths) == len(d[losing_team]) - 1
        ):  # If someone hasn't died on the losing team
            for player in d[losing_team]:
                died = False
                for death in deaths:
                    if player["name"] == death["name"]:
                        died = True
                if not died:  # For the person who didn't die
                    if (i <= 12 and losing_team == "Red") or (
                        i > 12 and losing_team == "Blue"
                    ):  # If they're an attacker
                        # TODO might be not a bitch move, i.e. saving.
                        player["pussy_score"] += 1
                    else:  # If they're a defender
                        if (
                            round["plant_events"]["plant_time_in_round"]
                            < deaths[-1]["time"]
                        ):  # Has to have been planted for a loss
                            player["rotate_score"] += 1
                    break
    d["Red"].sort(key=lambda p: p["pussy_score"] + p["rotate_score"], reverse=True)
    d["Blue"].sort(key=lambda p: p["pussy_score"] + p["rotate_score"], reverse=True)
    return d


def get_online_players():
    online = []
    for player in get_player_list()["players"]:
        online.append(
            (
                f"{player['name']}#{player['tag']}",
                api.get_online1(f"{player['name']}#{player['tag']}"),
            )
        )
    return online


def last_to_die_test():
    with open("sample_comp_game.txt.txt") as f:
        data = json.load(f)

    # for match in data['data']['matches']:
    #     print(last_to_die(match))
    return data


# for team in last_to_die_test().values():
#     print(team)
#     for player in team:
#         print(player)
#         print(f'{player["name"]}',f':scream_cat:: {player["pussy_score"]}\n:sloth:: {player["rotate_score"]}')
# print(last_to_die_test())

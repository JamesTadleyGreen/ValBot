import api
import json

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

def remove_player_from_list(player: str):
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

def update_players_info():
    print("Updating info")
    with open('player_list.txt', 'r+') as f:
        json_data = json.load(f)
        for player in json_data['players']:
            player_id = f"{player['name']}#{player['tag']}"
            rank_data = api.get_player_rank(player_id)
            last_online = api.check_last_online(player_id)
            if rank_data is not None:
                player['rank_data'] = rank_data
            if last_online is not None:
                player['last_online'] = last_online
        f.truncate(0)
        f.seek(0)
        f.write(json.dumps(json_data, indent=4))
        return "Done."

#update_players_info()
#add_player_to_list("SUGAH WURM#8630")
#update_players_info()
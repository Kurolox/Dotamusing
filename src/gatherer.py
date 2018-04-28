import requests
from datetime import datetime


def fetch_data(steamID):
    """Calls all the other functions that fetch relevant info for the profile, and formats them in a dict."""
    data_dict = {}
    data_dict["profile"] = get_user_profile(steamID)
    data_dict["match_history"] = full_match_history(steamID)
    return data_dict


def get_user_profile(steamID):
    """Fetches the profile info from the OpenDota API"""
    try:
        return requests.get(f"https://api.opendota.com/api/players/{steamID}").json()
    except ValueError:
        return {}


def full_match_history(steamID):
    full_match_history = {}
    match_history = requests.get(
        f"https://api.opendota.com/api/players/{steamID}/matches?project=heroes").json()
    full_match_history["totaltime"] = format(sum(
        [match["duration"] for match in match_history]) / 3600, ".1f")  # Seconds to hours
    full_match_history["totalgames"] = len(match_history)
    full_match_history["averagetime"] = format(
        60 * float(full_match_history["totaltime"]) / full_match_history["totalgames"], ".1f")
    full_match_history["rarestinfo"] = gather_rarest(match_history)

    return full_match_history


def gather_rarest(match_history):
    """Generates a dict with info to display regarding the hero you haven't seen for the longest time"""
    rarest_dict = {}
    rarest_dict["raresthero"] = find_rarest_hero(match_history)
    rarest_dict["gameID"] = hero_lastgame_ID(
        match_history, rarest_dict["raresthero"])
    rarest_dict["game_json"] = requests.get(
        f"https://api.opendota.com/api/matches/{rarest_dict['gameID']}").json()
    rarest_dict["date"] = datetime.fromtimestamp(
        rarest_dict["game_json"]["start_time"]).strftime("%d %B, %Y")
    rarest_dict["timediff"] = format(((int(datetime.now().timestamp(
    ))) - rarest_dict["game_json"]["start_time"]) / (3600 * 24), ".1f")
    rarest_dict["heroinfo"] = requests.get("https://raw.githubusercontent.com/odota/dotaconstants/master/build/heroes.json").json()[str(rarest_dict["raresthero"])]
    rarest_dict["portrait"] = f"http://cdn.dota2.com/apps/dota2/images/heroes/{rarest_dict['heroinfo']['img'].split('/')[-1]}"
    return rarest_dict


def find_rarest_hero(match_history):
    """Checks which hero haven't you seen in one of your games (in both teams) for the longest time"""
    hero_id_list = []
    for game in match_history:
        for hero in game["heroes"]:
            if game["heroes"][hero]["hero_id"] not in hero_id_list:
                # Adds all heroes to the list sequentially, being the last in the list the one you haven't seen in the longest time
                hero_id_list.append(game["heroes"][hero]["hero_id"])
    try:
        # If for some reason there's an ID 0 in the list, remove it
        hero_id_list.remove(0)
    except ValueError:
        pass
    return hero_id_list[-1]


def hero_lastgame_ID(match_history, heroID):
    """Gets the ID of the newest match where heroID was present in any time."""
    for game in match_history:
        for hero in game["heroes"]:
            if game["heroes"][hero]["hero_id"] == heroID:
                return game["match_id"]
    return None

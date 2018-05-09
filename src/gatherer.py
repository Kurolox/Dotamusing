import requests
from datetime import datetime
from collections import defaultdict
import json
from os.path import realpath, dirname


class user():
    def __init__(self, steamID):
        self._profile = requests.get(
            f"https://api.opendota.com/api/players/{steamID}").json()
        print("API Request made (User self._profile)")
        self._match_history = requests.get(
            f"https://api.opendota.com/api/players/{steamID}/matches?project=heroes").json()
        print("API Request made (User self._match_history)")

    def get_profile(self):
        """Returns the OpenDota profile data of the user."""
        return self._profile["profile"]

    def get_steamID(self):
        """Returns the Steam32 ID of the user."""
        return self.get_profile()["account_id"]

    def get_match_history(self):
        """Returns a list of all the matches of the user."""
        return self._match_history

    def get_avatar(self):
        """Returns a link to the user avatar."""
        return self.get_profile()["avatarfull"]

    def get_username(self):
        """Gets the display name of the user."""
        return self.get_profile()["personaname"]

    def total_playtime(self):
        """Returns the total hours of in-game playtime."""
        # Seconds to hours
        return float(format(sum([match["duration"] for match in self.get_match_history()]) / 3600, ".1f"))

    def match_count(self):
        """Returns the total number of matches played."""
        return len(self.get_match_history())

    def average_playtime(self):
        """Returns the average time of a match in minutes."""
        return float(format(60 * self.total_playtime() / self.match_count(), ".1f"))

    def get_recent_match(self, hero):
        """Gets the ID of the most recent match where the hero was present in any time."""
        for game in self.get_match_history():  # TODO: Improve this function with a single check
            for hero_slot in game["heroes"]:
                if game["heroes"][hero_slot]["hero_id"] == hero.get_heroID():
                    return match(game["match_id"])

    def find_rarest_heroes(self):
        """Checks which heroes haven't you seen in one of your games (in both teams) for the longest time"""
        hero_id_list = []
        for game in self.get_match_history():
            for hero_slot in game["heroes"]:
                if game["heroes"][hero_slot]["hero_id"] not in hero_id_list:
                    # Adds all heroes to the list sequentially, being the last in the list the one you haven't seen in the longest time
                    hero_id_list.append(game["heroes"][hero_slot]["hero_id"])
        try:  # If there's a 0 in the list, remove it.
            hero_id_list.remove(0)
        except ValueError:  # If there isn't, just ignore it.
            pass
        return [hero(rare_hero) for rare_hero in hero_id_list]

    def find_least_seen_heroes(self):
        """Returns an ordered list of the ID's of the heroes you've seen the least in all your games."""
        times_hero_seen = defaultdict(int)
        for game in self.get_match_history():
            for hero_slot in game["heroes"]:
                times_hero_seen[int(game["heroes"][hero_slot]["hero_id"])] += 1
        return [(hero(least_hero), times_seen) for least_hero, times_seen in sorted(times_hero_seen.items(), key=lambda x: x[1])]


class hero():
    def __init__(self, heroID):
        with open(f"{dirname(realpath(__file__))}/static/json/heroes.json", "r") as hero_json:
            self._constant_data = json.load(hero_json)[str(heroID)]
        
    def get_constant_data(self):
        """returns the data gathered by opendota about the hero."""
        return self._constant_data

    def get_heroID(self):
        """returns the ID of the hero."""
        return self.get_constant_data()["id"]

    def get_hero_portrait(self):
        """Returns an URL to the portrait image of the hero."""
        return f"http://cdn.dota2.com{self.get_constant_data()['img']}"

    def get_hero_name(self):
        """Returns the name of the hero."""
        return self.get_constant_data()["localized_name"]


class match():
    def __init__(self, matchID):
        self._opendota_data = requests.get(
            f"https://api.opendota.com/api/matches/{matchID}").json()
        print("API Request made (match self._opendota_data)")

    def get_opendota_data(self):
        """Returns the data gathered by opendota about the match."""
        return self._opendota_data

    def get_match_ID(self):
        return self.get_opendota_data()["match_id"]

    def get_match_timestamp(self):
        return self.get_opendota_data()["start_time"]

    def get_opendota_link(self):
        """Returns a link to the match in opendota."""
        return f"https://www.opendota.com/matches/{self.get_match_ID()}"

    def get_match_date(self):
        """Returns the date of the match, in format """  # 'TODO: Fill format example
        return datetime.fromtimestamp(self.get_match_timestamp()).strftime("%d %B, %Y")

    def get_match_time_difference(self):
        """Returns the time difference in days between the match date and the current time."""
        return int((int(datetime.now().timestamp()) - self.get_match_timestamp()) / (3600 * 24))

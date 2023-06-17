import json
import os
import time
from datetime import datetime

import requests

from trakt import EpisodeSearch, Season

HOST = "https://api.trakt.tv"
USER_AGENT = "trakt-to-sqlite"
CLIENT_ID = os.environ["TRAKT_API_CLIENT_ID"]
MAXSIZE = 100000
WAIT_TIME = 1  # second


class TraktRequest:
    def __init__(self, username: str, backup_path: str, api_key: str = CLIENT_ID):
        self.username = username
        self.backup_url = f"{HOST}/users/{self.username}"
        self.root_path = backup_path
        timestamp = datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H%M%S")
        self.backup_dir = f"backup\\{self.username}\\{timestamp}"
        self.backup_path = os.path.join(self.root_path, self.backup_dir)
        self.headers = {
            "Content-Type": "application/json",
            "trakt-api-version": "2",
            "trakt-api-key": api_key,
            "user-agent": USER_AGENT,
        }

    def get_show_data_from_episode_id(self, id: int) -> EpisodeSearch:
        URL = f"{HOST}/search/trakt/{id}?type=episode"
        print(f"Fetching : {URL}")
        r = requests.get(URL, headers=self.headers)

        if r.status_code == 200:
            data = r.content.decode()
            return json.loads(data[1:-1])
        else:
            raise Exception(
                f"An error as occurred with code: {r.status_code} for operation"
                " search episode data."
            )

    def get_seasons_data_from_show_id(self, show_id: int) -> list[Season]:
        URL = f"{HOST}/shows/{show_id}/seasons?extended=episodes"
        print(f"Fetching : {URL}")
        r = requests.get(URL, headers=self.headers)

        if r.status_code == 200:
            data = r.content.decode()
            seasons: list[Season] = json.loads(data)
            return seasons
        else:
            raise Exception(
                f"An error as occurred with code: {r.status_code} for operation"
                " search episode data."
            )

    def fetch(self, item: str, endpoint: str):
        print(f"Fetching : {self.backup_url}/{item}/{endpoint}")
        response = requests.get(
            f"{self.backup_url}/{item}/{endpoint}?limit={MAXSIZE}", headers=self.headers
        )

        if response.status_code == 404:
            raise Exception(f"Error: user {self.username} not found")
        elif response.status_code != 200:
            print(
                f"An error as occurred with code: {response.status_code} for operation"
                f" {item}/{endpoint}"
            )
            return

        if not response.json():
            print(f"No {endpoint} found in {item}")
            return

        if not os.path.isdir(self.backup_path):
            os.makedirs(self.backup_path)

        out_file_path = os.path.join(self.backup_path, f"{item}_{endpoint}.json")
        print(f"Writing to : {out_file_path}")
        with open(out_file_path, "w") as fh:
            fh.write(json.dumps(response.json(), separators=(",", ":"), indent=4))
        print(f"Completed : {self.backup_url}/{item}/{endpoint}")

    def get_watched_movies(self):
        self.fetch("watched", "movies")

    def get_watched_episodes(self):
        self.fetch("watched", "episodes")

    def get_watched_shows(self):
        self.fetch("watched", "shows")

    def get_movies_ratings(self):
        self.fetch("ratings", "movies")

    def get_episodes_ratings(self):
        self.fetch("ratings", "episodes")

    def get_shows_ratings(self):
        self.fetch("ratings", "shows")

    def get_seasons_ratings(self):
        self.fetch("ratings", "seasons")

    def get_movies_history(self):
        self.fetch("history", "movies")

    def get_episodes_history(self):
        self.fetch("history", "episodes")

    def get_movies_watchlist(self):
        self.fetch("watchlist", "movies")

    def get_shows_watchlist(self):
        self.fetch("watchlist", "shows")

    def get_movies_collection(self):
        self.fetch("collection", "movies")

    def get_episodes_collection(self):
        self.fetch("collection", "episodes")

    def get_shows_collection(self):
        self.fetch("collection", "shows")

    def get_user_stats(self):
        self.fetch("stats", "")

    def backup(self):
        print(f"Starting backup for user : {self.username}")
        start = time.time()
        self.get_watched_movies()
        self.get_watched_episodes()
        self.get_watched_shows()
        self.get_movies_ratings()
        self.get_episodes_ratings()
        self.get_shows_ratings()
        self.get_seasons_ratings()
        self.get_movies_history()
        self.get_episodes_ratings()
        self.get_movies_watchlist()
        self.get_episodes_history()
        self.get_shows_watchlist()
        self.get_movies_collection()
        self.get_episodes_collection()
        self.get_shows_collection()
        self.get_user_stats()
        print(f"Completed all operations in {round(time.time() - start, 2)} seconds.")

    def test_connection(self) -> bool:
        response = requests.get(f"{self.backup_url}/stats", headers=self.headers)
        return response.status_code == 200

    def wait(self):
        time.sleep(WAIT_TIME)

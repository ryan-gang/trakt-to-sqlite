import json
import os
import time
from datetime import datetime

import requests

HOST = "https://api.trakt.tv/users"
USER_AGENT = "trakt-to-sqlite"
CLIENT_ID = os.environ["TRAKT_API_CLIENT_ID"]
MAXSIZE = 100000


class TraktRequest:
    def __init__(self, username: str, api_key: str = CLIENT_ID):
        self.username = username
        self.url = f"{HOST}/{self.username}"
        self.root_path = os.getcwd()
        timestamp = datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H%M%S")
        self.backup_dir = f"backup\\{self.username}\\{timestamp}"
        self.backup_path = os.path.join(self.root_path, self.backup_dir)
        if not os.path.isdir(self.backup_path):
            os.makedirs(self.backup_path)
        self.headers = {
            "Content-Type": "application/json",
            "trakt-api-version": "2",
            "trakt-api-key": api_key,
            "user-agent": USER_AGENT,
        }

    def fetch(self, item: str, endpoint: str):
        print(f"Fetching : {self.url}/{item}/{endpoint}")
        response = requests.get(
            f"{self.url}/{item}/{endpoint}?limit={MAXSIZE}", headers=self.headers
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

        out_file_path = os.path.join(self.backup_path, f"{item}_{endpoint}.json")
        print(f"Writing to : {out_file_path}")
        with open(out_file_path, "w") as fh:
            fh.write(json.dumps(response.json(), separators=(",", ":"), indent=4))
        print(f"Completed : {self.url}/{item}/{endpoint}")

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


if __name__ == "__main__":
    t = TraktRequest(username="foo")
    t.backup()

import argparse
from sqlite_utils import Database
import os
from parse import Collected, Commons

from support import load_json
from api import TraktRequest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="trakt-to-sqlite")
    parser.add_argument(
        "--username",
        "-u",
        type=str,
        help="Pass the trakt username, for backing up data.",
    )
    parser.add_argument(
        "--backuppath",
        "-p",
        type=str,
        help=(
            "Pass the location where the backed up files will be stored, and the sqlite database"
            " created."
        ),
    )

    args = parser.parse_args()
    if PATH := args.backuppath:
        if not os.path.isdir(PATH):
            os.makedirs(PATH)
    username = args.username
    db_path = os.path.join(PATH, f"{username}.db")
    db = Database(db_path)

    cl = Collected()
    c = Commons()
    api = TraktRequest(username, backup_path=PATH)
    api.backup()

    # HANDLING COLLECTED EPISODES AND MOVIES.

    data = load_json(rf"backup\{username}\collection_episodes.json")
    shows_data = load_json(rf"backup\{username}\collection_shows.json")

    cl.handle_collected_episodes_prerequisites(shows_data, db, username)
    c_eps = list(map(cl.handle_collected_episode_entry, data))
    db["collected"].insert_all(c_eps, hash_id="id", ignore=True)  # type: ignore

    movie_data = load_json(rf"backup\{username}\collection_movies.json")

    cl.handle_collected_movies_prerequisites(movie_data, db)
    ms = list(map(cl.handle_collected_movie_entry, movie_data))
    db["collected"].insert_all(ms, hash_id="id", ignore=True)  # type: ignore

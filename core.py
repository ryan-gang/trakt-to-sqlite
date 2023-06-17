"""
core.py contains the high level functions that will be directly called from the main method,
and also will be exposed to users for usage.
"""
import os

from sqlite_utils import Database

from api import TraktRequest
from parse import Collected, Rated
from support import load_json


def save_ratings_files(db: Database, PATH: str):
    """
    `PATH` should contain all the backed up json files from trakt.
    This method takes that `path`, and a `sqlite connection` to parse the files
    that contain `ratings` in their name and writes them to the `ratings` table in the db.
    """
    files = os.listdir(PATH)
    files = list(filter(lambda x: "ratings" in x, files))

    r = Rated()

    for file_name in files:
        file_path = os.path.join(PATH, file_name)
        if "episodes" in file_name:
            data = load_json(file_path)
            episode_ratings = list(map(r.entry_to_rated_episode_row, data))
            db["ratings"].insert_all(episode_ratings, hash_id="id", ignore=True, batch_size=100)  # type: ignore
        elif "shows" in file_name:
            data = load_json(file_path)
            show_ratings = list(map(r.entry_to_rated_show_row, data))
            db["ratings"].insert_all(show_ratings, hash_id="id", ignore=True, batch_size=100)  # type: ignore
        elif "movies" in file_name:
            data = load_json(file_path)
            movie_ratings = list(map(r.entry_to_rated_movie_row, data))
            db["ratings"].insert_all(movie_ratings, hash_id="id", ignore=True, batch_size=100)  # type: ignore


def save_collections_files(db: Database, PATH: str, api: TraktRequest):
    """
    `PATH` should contain all the backed up json files from trakt.
    This method takes that `path`, and a `sqlite connection` to parse the files
    that contain `collection` in their name and writes them to the `collected` table in the db.
    """
    files = os.listdir(PATH)
    files = list(filter(lambda x: "collection" in x, files))

    cl = Collected()
    data = show_data = movie_data = ""

    for file_name in files:
        file_path = os.path.join(PATH, file_name)
        if "episodes" in file_name:
            data = load_json(file_path)
        elif "shows" in file_name:
            show_data = load_json(file_path)
        elif "movies" in file_name:
            movie_data = load_json(file_path)

    if data and show_data and movie_data:
        cl.handle_collected_episodes_prerequisites(show_data, db, api)
        c_eps = list(map(cl.handle_collected_episode_entry, data))
        db["collected"].insert_all(c_eps, hash_id="id", ignore=True)  # type: ignore

        cl.handle_collected_movies_prerequisites(movie_data, db)
        movies = list(map(cl.handle_collected_movie_entry, movie_data))
        db["collected"].insert_all(movies, hash_id="id", ignore=True)  # type: ignore

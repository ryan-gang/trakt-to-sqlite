import json
import os

from sqlite_utils import Database

from trakt import Episode, EpisodeRow, HistoryEpisode, HistoryEpisodeRow, Show, ShowRow

USERNAME = "######"
FILE = rf"backup\{USERNAME}\history_episodes.json"
# FILE = fr"backup\{USERNAME}\history_movies.json"
assert os.path.isfile(FILE)


with open(FILE, "r") as f:
    data = json.load(f)


# Parse API Data to python data structures.
def entry_to_history_episode_row(entry: HistoryEpisode) -> HistoryEpisodeRow:
    return {
        "id": entry["id"],
        "episode_id": entry["episode"]["ids"]["trakt"],
        "watched_at": entry["watched_at"],
    }


def entry_to_episode(entry: HistoryEpisode) -> Episode:
    return entry["episode"]


def entry_to_show(entry: HistoryEpisode) -> Show:
    return entry["show"]


def get_show_id_from_entry(entry: HistoryEpisode) -> int:
    return entry["show"]["ids"]["trakt"]


def entry_to_episode_row(entry: Episode, show_id: int) -> EpisodeRow:
    return {
        "type": "episode",
        "id": entry["ids"]["trakt"],
        "show_id": show_id,
        "season": entry["season"],
        "number": entry["number"],
        "title": entry["title"],
        "trakt_id": entry["ids"]["trakt"],
        "tvdb_id": entry["ids"]["tvdb"],
        "imdb_id": entry["ids"]["imdb"],
        "tmdb_id": entry["ids"]["tmdb"],
        "tvrage_id": entry["ids"]["tvrage"],
    }


def entry_to_show_row(entry: Show) -> ShowRow:
    return {
        "type": "show",
        "id": entry["ids"]["trakt"],
        "title": entry["title"],
        "year": entry["year"],
        "trakt_id": entry["ids"]["trakt"],
        "trakt_slug": entry["ids"]["slug"],
        "tvdb_id": entry["ids"]["tvdb"],
        "imdb_id": entry["ids"]["imdb"],
        "tmdb_id": entry["ids"]["tmdb"],
        "tvrage_id": entry["ids"]["tvrage"],
    }


def handle_history_episode_entry(
    entry: HistoryEpisode,
) -> tuple[HistoryEpisodeRow, EpisodeRow, ShowRow]:
    h_ep_row = entry_to_history_episode_row(entry)
    show_id = get_show_id_from_entry(entry)
    ep_row = entry_to_episode_row(entry_to_episode(entry), show_id)
    s_row = entry_to_show_row(entry_to_show(entry))
    return (h_ep_row, ep_row, s_row)


episodes = [i[1] for i in list(map(handle_history_episode_entry, data))]
watchlog = [i[0] for i in list(map(handle_history_episode_entry, data))]
shows = [i[2] for i in list(map(handle_history_episode_entry, data))]

db = Database(f"{USERNAME}.db")
assert all(
    [True for table in ["show", "episode", "episode_watchlog"] if table in db.table_names()]
), "All of the tables are not created."

db["show"].insert_all(shows, pk="id", ignore=True, batch_size=100)  # type: ignore

db["episode"].insert_all(episodes, pk="id", ignore=True, batch_size=100, foreign_keys=["show_id"])  # type: ignore

db["episode_watchlog"].insert_all(watchlog, ignore=True, batch_size=100, foreign_keys=["episode_id"])  # type: ignore

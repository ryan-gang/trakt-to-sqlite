from itertools import repeat
from typing import Optional

from sqlite_utils import Database

from api import TraktRequest
from trakt import (
    CollectedEpisode,
    CollectedEpisodeRow,
    Episode,
    EpisodeRow,
    HistoryEpisode,
    HistoryEpisodeRow,
    HistoryMovie,
    HistoryMovieRow,
    Movie,
    MovieRow,
    Season,
    Show,
    ShowRow,
)


class Commons:
    def episode_to_episode_row(self, entry: Episode, show_id: int) -> EpisodeRow:
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

    def show_to_show_row(self, entry: Show) -> ShowRow:
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

    def multiple_seasons_to_list_episode_row(self, entry: list[Season]) -> list[EpisodeRow]:
        # return list(map(self.season_to_episode_rows, entry)) # Gives 2D list.
        start: list[EpisodeRow] = []
        return sum(list(map(self.season_to_list_episode_row, entry)), start)

    def season_to_list_episode_row(self, entry: Season) -> list[EpisodeRow]:
        show_id = entry["ids"]["trakt"]
        episodes: list[Episode] = entry["episodes"]
        return list(map(self.episode_to_episode_row, episodes, repeat(show_id)))

    def movie_to_movie_row(self, entry: Movie) -> MovieRow:
        return {
            "type": "movie",
            "id": entry["ids"]["trakt"],
            "title": entry["title"],
            "year": entry["year"],
            "trakt_id": entry["ids"]["trakt"],
            "trakt_slug": entry["ids"]["slug"],
            "imdb_id": entry["ids"]["imdb"],
            "tmdb_id": entry["ids"]["tmdb"],
        }


class History:
    # Parse API Data, history_episodes to sqlite rows.
    def entry_to_history_episode_row(self, entry: HistoryEpisode) -> HistoryEpisodeRow:
        return {
            "id": entry["id"],
            "type": "episode",
            "media_id": entry["episode"]["ids"]["trakt"],
            "watched_at": entry["watched_at"],
        }

    def entry_to_episode(self, entry: HistoryEpisode) -> Episode:
        return entry["episode"]

    def entry_to_show(self, entry: HistoryEpisode) -> Show:
        return entry["show"]

    def get_show_id_from_entry(self, entry: HistoryEpisode) -> int:
        return entry["show"]["ids"]["trakt"]

    def handle_history_episode_entry(
        self,
        entry: HistoryEpisode,
    ) -> tuple[HistoryEpisodeRow, EpisodeRow, ShowRow]:
        c = Commons()
        h_ep_row = self.entry_to_history_episode_row(entry)
        show_id = self.get_show_id_from_entry(entry)
        ep_row = c.episode_to_episode_row(self.entry_to_episode(entry), show_id)
        s_row = c.show_to_show_row(self.entry_to_show(entry))
        return (h_ep_row, ep_row, s_row)

    # Parse API Data, history_movies to sqlite rows.
    def entry_to_history_movie_row(self, entry: HistoryMovie) -> HistoryMovieRow:
        return {
            "id": entry["id"],
            "type": "movie",
            "media_id": entry["movie"]["ids"]["trakt"],
            "watched_at": entry["watched_at"],
        }

    def entry_to_movie(self, entry: HistoryMovie) -> Movie:
        return entry["movie"]

    def handle_history_movie_entry(
        self,
        entry: HistoryMovie,
    ) -> tuple[HistoryMovieRow, MovieRow]:
        c = Commons()
        h_m_row = self.entry_to_history_movie_row(entry)
        m_row = c.movie_to_movie_row(self.entry_to_movie(entry))
        return (h_m_row, m_row)


class Collected:
    # Parse API Data, collected_episodes to sqlite rows.
    def entry_to_collected_episode_row(self, entry: CollectedEpisode) -> CollectedEpisodeRow:
        return {
            "type": "episode",
            "media_id": entry["episode"]["ids"]["trakt"],
            "collected_at": entry["collected_at"],
        }

    def entry_to_episode(self, entry: CollectedEpisode) -> Episode:
        return entry["episode"]

    def get_episode_id_from_entry(self, entry: CollectedEpisode) -> int:
        return entry["episode"]["ids"]["trakt"]

    def entry_to_episode_row(self, entry: Episode, show_id: int) -> EpisodeRow:
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

    def handle_collected_episode_entry_deprecated(
        self, entry: CollectedEpisode, db: Database, username: str
    ) -> tuple[CollectedEpisodeRow, list[EpisodeRow], Optional[ShowRow]]:
        """
        This approach was not working, there is an inherent flaw in the sqlite_utils library where insert() and consecutive insert_all() on the same database, but different tables throw an IndexError. And upsert() is not working idk why.
        So, the approach I settled on is handle the 3 parts seperately.
        First add all show data.
        Then for all the shows, get all the episodes add them.
        And finally the collected data.
        That works. Keeping this method as a backup just in case.
        """
        c = Commons()
        api = TraktRequest(username)

        episode_id = self.get_episode_id_from_entry(entry)
        logging.info(f"Starting hcee on episode_id : {episode_id}")
        # If episode is not present in our db, we can't get the show_id,
        # and in turn can't create a fully formed EpisodeRow.
        # So, we fetch the episode and show details from trakt API.
        # Write the entire show history to our db, so as to not poll the API again.
        episodes = []
        logging.info(
            "count of episode_id in episode table:"
            f" {db['episode'].count_where('id == ?', [episode_id])}"
        )

        flag = False
        if db["episode"].count_where("id == ?", [episode_id]) < 1:  # type :ignore
            flag = True
            logging.info(f"Inside if")
            show_data = api.get_show_data_from_episode_id(episode_id)
            logging.info(f"Got show data from api.")
            show_id = show_data["show"]["ids"]["trakt"]
            logging.info(f"show_id : {show_id}")
            show_row = c.show_to_show_row(show_data["show"])
            logging.info(show_row)
            seasons = api.get_seasons_data_from_show_id(show_id)
            logging.info(seasons)
            episodes = c.multiple_seasons_to_list_episode_row(seasons)
            logging.info(episodes)
            logging.info(f"Entire episodes_row is of length : {len(episodes)}")
        else:
            lst: list[EpisodeRow] = list(db["episode"].rows_where("id == ?", [episode_id]))
            assert len(lst) == 1
            logging.info(f"Inside else condition")
            logging.info(lst)
            show_id = lst[0]["show_id"]
            logging.info(show_id)
            show_row = None
            logging.info("As show_id is present in table, show_row is None.")
        cl_episode_row = self.entry_to_collected_episode_row(entry)
        logging.info(f"Converted CollectedEpisode to CollectedEpisodeRow : {cl_episode_row}")
        episode_row = c.episode_to_episode_row(self.entry_to_episode(entry), show_id)
        logging.info(f"Current episode from data got from the json file : {episode_row}")
        if not flag:
            episodes.append(episode_row)
            logging.info(f"Entire episodes_row is now of length : {len(episodes)}")

        return (cl_episode_row, episodes, show_row)

    def handle_collected_episodes_prerequisites(self, data, db: Database, username: str) -> None:
        c = Commons()

        show_ids: list[int] = []
        show_rows: list[ShowRow] = []
        for entry in data:
            show_id: int = entry["show"]["ids"]["trakt"]
            show: Show = entry["show"]
            show_ids.append(show_id)
            show_rows.append(c.show_to_show_row(show))

        db["show"].insert_all(show_rows, pk="id", batch_size=100, ignore=True)  # type: ignore

        api = TraktRequest(username="tinydino")
        for show_id in show_ids:
            seasons = api.get_seasons_data_from_show_id(show_id)
            episodes = c.multiple_seasons_to_list_episode_row(seasons)
            db["episode"].insert_all(
                episodes, pk="id", foreign_keys=["show_id"], batch_size=100, ignore=True
            )

    def handle_collected_episode_entry(self, entry: CollectedEpisode) -> CollectedEpisodeRow:
        cl_episode_row = self.entry_to_collected_episode_row(entry)
        return cl_episode_row

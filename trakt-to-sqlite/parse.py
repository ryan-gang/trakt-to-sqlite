from itertools import repeat

from api import TraktRequest
from sqlite_utils import Database
from trakt import (CollectedEpisode, CollectedEpisodeRow, CollectedMovie,
                   CollectedMovieRow, CollectedShow, Episode, EpisodeRow,
                   ExtendedEpisode, ExtendedEpisodeRow, ExtendedMovie,
                   ExtendedMovieRow, ExtendedShow, ExtendedShowRow,
                   HistoryEpisode, HistoryEpisodeRow, HistoryMovie,
                   HistoryMovieRow, Movie, MovieRow, RatedEpisode,
                   RatedEpisodeRow, RatedMovie, RatedMovieRow, RatedShow,
                   RatedShowRow, Season, Show, ShowRow, WatchlistMovie,
                   WatchlistMovieRow, WatchlistShow, WatchlistShowRow)


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

    def multiple_seasons_to_list_episode_row(
        self, entry: list[Season], show_id: int
    ) -> list[EpisodeRow]:
        # The season's data actually contains the id of the season.
        # So, we need to replace that id with the actual show_id.
        # return list(map(self.season_to_episode_rows, entry)) # Gives 2D list.
        start: list[EpisodeRow] = []

        return sum(list(map(self.season_to_list_episode_row, entry, repeat(show_id))), start)

    def season_to_list_episode_row(self, entry: Season, show_id: int) -> list[EpisodeRow]:
        # season_id = entry["ids"]["trakt"]
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

    def generate_genres(self, db: Database, api: TraktRequest) -> str:
        g = api.get_genre_data()
        db["genre"].insert_all(g, hash_id="id", batch_size=50, ignore=True)  # type: ignore
        return f"Added {len(list(db['genre'].rows))} genres to genre table."  # type: ignore

    def extended_episode_to_extended_episode_row(
        self, entry: ExtendedEpisode, show_id: int
    ) -> ExtendedEpisodeRow:
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
            "overview": entry["overview"],
            "rating": entry["rating"],
            "votes": entry["votes"],
            "comment_count": entry["comment_count"],
            "first_aired": entry["first_aired"],
            "runtime": entry["runtime"],
        }

    def extended_show_to_extended_show_row(self, entry: ExtendedShow) -> ExtendedShowRow:
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
            "overview": entry["overview"],
            "first_aired": entry["first_aired"],
            "runtime": entry["runtime"],
            "certification": entry["certification"],
            "network": entry["network"],
            "country": entry["country"],
            "trailer": entry["trailer"],
            "homepage": entry["homepage"],
            "status": entry["status"],
            "language": entry["language"],
            "aired_episodes": entry["aired_episodes"],
            "rating": entry["rating"],
            "votes": entry["votes"],
            "comment_count": entry["comment_count"],
        }

    def extended_movie_to_extended_movie_row(self, entry: ExtendedMovie) -> ExtendedMovieRow:
        return {
            "type": "movie",
            "id": entry["ids"]["trakt"],
            "title": entry["title"],
            "year": entry["year"],
            "trakt_id": entry["ids"]["trakt"],
            "trakt_slug": entry["ids"]["slug"],
            "imdb_id": entry["ids"]["imdb"],
            "tmdb_id": entry["ids"]["tmdb"],
            "tagline": entry["tagline"],
            "overview": entry["overview"],
            "released": entry["released"],
            "runtime": entry["runtime"],
            "country": entry["country"],
            "trailer": entry["trailer"],
            "homepage": entry["homepage"],
            "status": entry["status"],
            "rating": entry["rating"],
            "votes": entry["votes"],
            "comment_count": entry["comment_count"],
            "language": entry["language"],
            "certification": entry["certification"],
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
        return h_ep_row, ep_row, s_row

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
        return h_m_row, m_row


class Collected:
    # Parse API Data, collected_episodes to sqlite rows.
    def entry_to_collected_episode_row(self, entry: CollectedEpisode) -> CollectedEpisodeRow:
        return {
            "type": "episode",
            "media_id": entry["episode"]["ids"]["trakt"],
            "collected_at": entry["collected_at"],
        }

    def entry_to_collected_movie_row(self, entry: CollectedMovie) -> CollectedMovieRow:
        return {
            "type": "movie",
            "media_id": entry["movie"]["ids"]["trakt"],
            "collected_at": entry["collected_at"],
        }

    def entry_to_episode(self, entry: CollectedEpisode) -> Episode:
        return entry["episode"]

    def entry_to_movie(self, entry: CollectedMovie) -> Movie:
        return entry["movie"]

    def get_episode_id_from_entry(self, entry: CollectedEpisode) -> int:
        return entry["episode"]["ids"]["trakt"]

    def entry_to_episode_row(self, entry: Episode, show_id: int) -> EpisodeRow:
        return Commons().episode_to_episode_row(entry, show_id)

    def handle_collected_episodes_prerequisites(
        self, show_data: list[CollectedShow], db: Database, api: TraktRequest
    ) -> None:
        c = Commons()

        show_ids: list[int] = []
        show_rows: list[ShowRow] = []
        for entry in show_data:
            show_id: int = entry["show"]["ids"]["trakt"]
            show: Show = entry["show"]
            show_ids.append(show_id)
            show_rows.append(c.show_to_show_row(show))

        db["show"].insert_all(show_rows, pk="id", batch_size=100, ignore=True)  # type: ignore

        for show_id in show_ids:
            seasons = api.get_season_data(show_id)
            episodes = c.multiple_seasons_to_list_episode_row(seasons, show_id)
            db["episode"].insert_all(  # type: ignore
                episodes,
                pk="id",  # type: ignore
                foreign_keys=["show_id"],  # type: ignore
                batch_size=100,  # type: ignore
                ignore=True,  # type: ignore
            )
            api.wait()

    def handle_collected_episode_entry(self, entry: CollectedEpisode) -> CollectedEpisodeRow:
        cl_episode_row = self.entry_to_collected_episode_row(entry)
        return cl_episode_row

    def handle_collected_movies_prerequisites(
        self, movie_data: list[CollectedMovie], db: Database
    ) -> None:
        c = Commons()
        movies = list(map(self.entry_to_movie, movie_data))
        movie_rows: list[MovieRow] = list(map(c.movie_to_movie_row, movies))

        db["movie"].insert_all(movie_rows, pk="id", batch_size=100, ignore=True)  # type: ignore

    def handle_collected_movie_entry(self, entry: CollectedMovie) -> CollectedMovieRow:
        cl_movie_row = self.entry_to_collected_movie_row(entry)
        return cl_movie_row


class Rated:
    # Parse API Data, rated_episodes to sqlite rows.
    def entry_to_rated_episode_row(self, entry: RatedEpisode) -> RatedEpisodeRow:
        return {
            "media_id": entry["episode"]["ids"]["trakt"],
            "type": "episode",
            "rating": entry["rating"],
            "rated_at": entry["rated_at"],
        }

    def entry_to_rated_show_row(self, entry: RatedShow) -> RatedShowRow:
        return {
            "media_id": entry["show"]["ids"]["trakt"],
            "type": "show",
            "rating": entry["rating"],
            "rated_at": entry["rated_at"],
        }

    def entry_to_rated_movie_row(self, entry: RatedMovie) -> RatedMovieRow:
        return {
            "media_id": entry["movie"]["ids"]["trakt"],
            "type": "movie",
            "rating": entry["rating"],
            "rated_at": entry["rated_at"],
        }


class Watchlist:
    # Parse API Data, watchlist_shows to sqlite rows.
    def entry_to_watchlisted_show_row(self, entry: WatchlistShow) -> WatchlistShowRow:
        return {
            "id": entry["id"],
            "media_id": entry["show"]["ids"]["trakt"],
            "type": "show",
            "watchlisted_at": entry["listed_at"],
        }

    def entry_to_watchlisted_movie_row(self, entry: WatchlistMovie) -> WatchlistMovieRow:
        return {
            "id": entry["id"],
            "media_id": entry["movie"]["ids"]["trakt"],
            "type": "movie",
            "watchlisted_at": entry["listed_at"],
        }

    def entry_to_show(self, entry: WatchlistShow) -> Show:
        return entry["show"]

    def entry_to_movie(self, entry: WatchlistMovie) -> Movie:
        return entry["movie"]

    def handle_watchlist_show_entry(
        self,
        entry: WatchlistShow,
    ) -> tuple[WatchlistShowRow, ShowRow]:
        c = Commons()
        show = self.entry_to_show(entry)
        show_row = c.show_to_show_row(show)
        watch_show_row = self.entry_to_watchlisted_show_row(entry)
        return watch_show_row, show_row

    def handle_watchlist_movie_entry(
        self,
        entry: WatchlistMovie,
    ) -> tuple[WatchlistMovieRow, MovieRow]:
        c = Commons()
        movie = self.entry_to_movie(entry)
        movie_row = c.movie_to_movie_row(movie)
        watch_movie_row = self.entry_to_watchlisted_movie_row(entry)
        return watch_movie_row, movie_row


class Extended:
    def __init__(self, db: Database, api: TraktRequest) -> None:
        self.db = db
        self.api = api

    def generate_genre_mapping(
        self,
    ) -> dict[str, str]:
        """
        Generate genre_name_to_id mapping.
        Reads in genre table from db, adds all the {name : id} pairs to a dict.
        """
        genre_name_to_id_mapping: dict[str, str] = {}
        for row in self.db["genre"].rows:  # type: ignore
            name: str = row["name"].lower().replace("-", " ")  # type: ignore
            genre_name_to_id_mapping[name] = row["id"]  # type: ignore

        return genre_name_to_id_mapping

    def generate_show_id_slug_mapping(
        self,
    ) -> dict[int, str]:
        """
        Generate show_id : show_slug mapping.
        Reads in show table from db, adds all the {id : slug} pairs to a dict.
        """
        show_id_to_slug_mapping: dict[int, str] = {}
        for row in self.db["show"].rows:  # type: ignore
            show_id_to_slug_mapping[row["id"]] = row["trakt_slug"]  # type: ignore

        return show_id_to_slug_mapping

    def handle_extended_movie(self):
        """
        For every row in the movie table, fetches the extended varsion of the data.
        (Provided it is not already present in the extended_movie table).
        Adds the genre mappings to the genre_mappings table, adds the
        extended movie data to the extended_movie table.
        """
        genre_name_to_id_mapping = self.generate_genre_mapping()
        extended_movie_ids: set[int] = set()
        all_rows: list[ExtendedMovieRow] = []
        all_genres: list[dict[str, str | int]] = []
        count = 0

        for row in self.db["extended_movie"].rows:  # type: ignore
            extended_movie_ids.add(row["id"])  # type: ignore
        try:
            count += 1
            for row in self.db["movie"].rows:  # type: ignore
                movie_slug, movie_id = row["trakt_slug"], row["id"]  # type: ignore
                if movie_id in extended_movie_ids:
                    print(f"{count}. Skipping {movie_slug}")
                    continue
                extended_data = self.api.get_extended_movie_data(movie_slug)  # type: ignore
                extended_data_row = Commons().extended_movie_to_extended_movie_row(extended_data)
                genres = extended_data["genres"]
                movie_id = extended_data_row["id"]
                for genre in genres:
                    genre_name = genre.lower().replace("-", " ")
                    genre_id = genre_name_to_id_mapping[genre_name]
                    g: dict[str, str | int] = {"media_id": movie_id, "genre_id": genre_id}
                    all_genres.append(g)

                print(f"{count}. {extended_data_row['title']}")
                all_rows.append(extended_data_row)
                self.api.wait(5)
        except Exception as e:
            print(f"Encountered exception : {e}")
        finally:
            self.db["extended_movie"].insert_all(all_rows, pk="id", batch_size=50)  # type: ignore
            print(f"Finished writing {len(all_rows)} rows into extended_movie table.")
            self.db["genre_mapping"].insert_all(all_genres, hash_id="id", ignore=True)  # type: ignore
            print(f"Finished writing {len(all_genres)} rows into genre_mapping table.")

    def handle_extended_show(self):
        """
        For every row in the show table, fetches the extended varsion of the data.
        (Provided it is not already present in the extended_show table).
        Adds the genre mappings to the genre_mappings table, adds the
        extended show data to the extended_show table.
        """
        genre_name_to_id_mapping = self.generate_genre_mapping()
        extended_show_ids: set[int] = set()
        all_rows: list[ExtendedShowRow] = []
        all_genres: list[dict[str, str | int]] = []
        count = 0

        for row in self.db["extended_show"].rows:  # type: ignore
            extended_show_ids.add(row["id"])  # type: ignore

        try:
            count += 1
            for row in self.db["show"].rows:  # type: ignore
                show_slug, show_id = row["trakt_slug"], row["id"]  # type: ignore
                if show_id in extended_show_ids:
                    print(f"{count}. Skipping {show_slug}")
                    continue
                extended_data = self.api.get_extended_show_data(show_slug)  # type: ignore
                extended_data_row = Commons().extended_show_to_extended_show_row(extended_data)
                genres = extended_data["genres"]
                show_id = extended_data_row["id"]
                for genre in genres:
                    genre_name = genre.lower().replace("-", " ")
                    genre_id = genre_name_to_id_mapping[genre_name]
                    g: dict[str, str | int] = {"media_id": show_id, "genre_id": genre_id}
                    all_genres.append(g)

                print(f"{count}. {extended_data_row['title']}")
                all_rows.append(extended_data_row)
                self.api.wait(10)
        except Exception as e:
            print(f"Encountered exception : {e}")
        finally:
            self.db["extended_show"].insert_all(all_rows, pk="id", ignore=True)  # type: ignore
            print(f"Finished writing {len(all_rows)} rows into extended_show table.")
            self.db["genre_mapping"].insert_all(all_genres, hash_id="id", ignore=True)  # type: ignore
            print(f"Finished writing {len(all_genres)} rows into genre_mapping table.")

    def handle_extended_episode(self):
        """
        For every row in the episode table, fetches the extended varsion of the data.
        (Provided it is not already present in the extended_episode table).
        Adds the genre mappings to the genre_mappings table, adds the
        extended episode data to the extended_episode table.
        """
        show_slug_id_mapping = self.generate_show_id_slug_mapping()
        extended_episode_ids: set[int] = set()
        all_rows: list[ExtendedEpisodeRow] = []
        count = 0

        for row in self.db["extended_episode"].rows:  # type: ignore
            extended_episode_ids.add(row["id"])  # type: ignore

        try:
            count += 1
            for row in self.db["episode"].rows:  # type: ignore
                episode_id, show_id, ep_season, ep_episode = map(
                    int,
                    (  # type: ignore
                        row["id"],
                        row["show_id"],
                        row["season"],
                        row["number"],
                    ),
                )
                show_slug = show_slug_id_mapping[show_id]
                if episode_id in extended_episode_ids:
                    print(f"{count}. Skipping {show_slug}-S{ep_season}-E{ep_episode}")
                    continue
                extended_data = self.api.get_extended_episode_data(show_slug, ep_season, ep_episode)
                extended_data_row = Commons().extended_episode_to_extended_episode_row(
                    extended_data, show_id
                )
                print(f"{count}. {show_slug}-S{ep_season}-E{ep_episode}")
                all_rows.append(extended_data_row)
                self.api.wait(10)
        except Exception as e:
            print(f"Encountered exception : {e}")
        finally:
            self.db["extended_episode"].insert_all(all_rows, pk="id", ignore=True)  # type: ignore
            print(f"Finished writing {len(all_rows)} rows into extended_episode table.")

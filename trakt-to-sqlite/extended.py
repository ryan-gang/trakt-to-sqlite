from api import TraktRequest
from parse import Commons
from sqlite_utils import Database
from trakt import ExtendedEpisodeRow, ExtendedMovieRow, ExtendedShowRow


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

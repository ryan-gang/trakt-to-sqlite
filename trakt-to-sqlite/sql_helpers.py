from typing import Callable, Generator, Any

from sqlite_utils import Database


class Datastore:
    def __init__(self, db: Database) -> None:
        self.db = db
        self.required_tables = [
            "show",
            "episode",
            "movie",
            "watchlog",
            "collected",
            "ratings",
            "watchlist",
            "genre",
            "extended_show",
            "extended_episode",
            "extended_movie",
            "genre_mapping",
        ]

        self.table_mapping: dict[str, Callable[[], None]] = {
            "show": self.create_show,
            "episode": self.create_episode,
            "movie": self.create_movie,
            "watchlog": self.create_watchlog,
            "collected": self.create_collected,
            "ratings": self.create_ratings,
            "watchlist": self.create_watchlist,
            "genre": self.create_genre,
            "extended_episode": self.create_extended_episode,
            "extended_movie": self.create_extended_movie,
            "extended_show": self.create_extended_show,
            "genre_mapping": self.create_genre_mapping,
        }

    def create_show(self):
        self.db["show"].create(  # type: ignore
            {
                "type": str,
                "id": int,
                "title": str,
                "year": int,
                "trakt_id": int,
                "trakt_slug": str,
                "tvdb_id": int,
                "imdb_id": str,
                "tmdb_id": int,
                "tvrage_id": int,
            },
            pk="id",
            not_null={"id", "title", "trakt_id"},
            defaults={"type": "show"},
        )

    def create_episode(self):
        self.db["episode"].create(  # type: ignore
            {
                "type": str,
                "id": int,
                "show_id": int,
                "season": int,
                "number": int,
                "title": str,
                "trakt_id": int,
                "tvdb_id": int,
                "imdb_id": str,
                "tmdb_id": int,
                "tvrage_id": int,
            },
            pk="id",
            not_null={"id", "season", "number", "trakt_id", "show_id"},
            defaults={"type": "episode"},
            foreign_keys=["show_id"],
        )

    def create_movie(self):
        self.db["movie"].create(  # type: ignore
            {
                "type": str,
                "id": int,
                "title": str,
                "year": int,
                "trakt_id": int,
                "trakt_slug": int,
                "imdb_id": str,
                "tmdb_id": int,
            },
            pk="id",
            not_null={"id", "title", "trakt_id"},
            defaults={"type": "movie"},
        )

    # Single table for all watched entities. (Movies and Episodes.)
    def create_watchlog(self):
        self.db["watchlog"].create(  # type: ignore
            {
                "id": int,
                "type": str,  # movie / episode
                "media_id": int,  # corresponding primary key of the entity.
                "watched_at": str,
            },
            pk="id",
            not_null={"id", "media_id", "watched_at"},
            # foreign_keys=["media_id"],
        )

        self.db.add_foreign_keys(
            [("watchlog", "media_id", "movie", "id"), ("watchlog", "media_id", "episode", "id")]
        )

    # Single table for all collected entities. (Movies and Episodes.)
    def create_collected(self):
        self.db["collected"].create(  # type: ignore
            {
                "id": str,
                "type": str,  # movie / episode
                "media_id": int,  # corresponding primary key of the entity.
                "collected_at": str,
            },
            pk="id",
            not_null={"id", "media_id", "collected_at"},
            # foreign_keys=["media_id"],
        )

        self.db.add_foreign_keys(
            [("collected", "media_id", "movie", "id"), ("collected", "media_id", "episode", "id")]
        )

    # Single table for all collected entities. (Movies and Episodes.)
    def create_ratings(self):
        self.db["ratings"].create(  # type: ignore
            {
                "id": str,
                "type": str,  # movie / episode / show
                "media_id": int,  # corresponding primary key of the entity.
                "rating": int,
                "rated_at": str,
            },
            pk="id",
            not_null={"id", "media_id", "rating"},
            # foreign_keys=["media_id"],
        )

        self.db.add_foreign_keys(
            [
                ("ratings", "media_id", "movie", "id"),
                ("ratings", "media_id", "episode", "id"),
                ("ratings", "media_id", "show", "id"),
            ]
        )

    # Single table for all watchlist-ed entities. (Movies and Shows.)
    def create_watchlist(self):
        self.db["watchlist"].create(  # type: ignore
            {
                "id": int,
                "type": str,  # movie / episode / show
                "media_id": int,  # corresponding primary key of the entity.
                "watchlisted_at": str,
            },
            pk="id",
            not_null={"id", "media_id", "watchlisted_at"},
            # foreign_keys=["media_id"],
        )

        self.db.add_foreign_keys(
            [
                ("watchlist", "media_id", "movie", "id"),
                ("watchlist", "media_id", "show", "id"),
            ]
        )

    def assert_tables(self) -> bool:
        return all(
            [True if table in self.db.table_names() else False for table in self.required_tables]
        )

    def create_tables(self) -> None:
        for table in self.required_tables:
            if table not in self.db.table_names():
                table_creation_func = self.table_mapping[table]
                table_creation_func()

    def get_shows_in_db(self) -> Generator[dict[str, str], Any, Any]:
        return self.db["show"].rows  # type: ignore

    def get_episodes_join_shows_in_db(self) -> Generator[dict[str, str], Any, Any]:
        return self.db.query("select E.id AS eid, E.season AS eseason, E.number AS enumber, E.title AS etitle, S.id, S.title, S.year, S.trakt_slug from episode E INNER JOIN show S on E.show_id = S.id")  # type: ignore

    def get_movies_in_db(self) -> Generator[dict[str, str], Any, Any]:
        return self.db["movie"].rows  # type: ignore

    # Single table for all genres.
    def create_genre(self):
        self.db["genre"].create(  # type: ignore
            {
                "id": str,
                "name": str,  # genre name
                "slug": str,  # genre slug
            },
            pk="id",
            not_null={"id", "name"},
        )

    # Single table for all media entities.
    # Media -> genre mapping.
    def create_genre_mapping(self):
        self.db["genre_mapping"].create(  # type: ignore
            {
                "id": str,
                "media_id": int,
                "genre_id": str,  # genre id
            },
            pk="id",
            not_null={"id", "media_id", "genre_id"},
        )

        self.db.add_foreign_keys(
            [
                ("genre_mapping", "media_id", "extended_show", "id"),
                ("genre_mapping", "media_id", "extended_movie", "id"),
                ("genre_mapping", "media_id", "extended_episode", "id"),
            ]
        )

    def create_extended_show(self):
        self.db["extended_show"].create(  # type: ignore
            {
                "type": str,
                "id": int,
                "title": str,
                "year": int,
                "trakt_id": int,
                "trakt_slug": str,
                "tvdb_id": int,
                "imdb_id": str,
                "tmdb_id": int,
                "tvrage_id": int,
                "overview": str,
                "first_aired": str,
                "runtime": int,
                "certification": str,
                "network": str,
                "country": str,
                "trailer": str,
                "homepage": str,
                "status": str,
                "language": str,
                "aired_episodes": int,
                "rating": float,
                "votes": int,
                "comment_count": int,
            },
            pk="id",
            not_null={"id", "title", "trakt_id"},
            defaults={"type": "show"},
        )

    def create_extended_episode(self):
        self.db["extended_episode"].create(  # type: ignore
            {
                "type": str,
                "id": int,
                "show_id": int,
                "season": int,
                "number": int,
                "title": str,
                "trakt_id": int,
                "tvdb_id": int,
                "imdb_id": str,
                "tmdb_id": int,
                "tvrage_id": int,
                "overview": str,
                "first_aired": str,
                "runtime": int,
                "certification": str,
                "network": str,
                "country": str,
                "trailer": str,
                "homepage": str,
                "status": str,
                "language": str,
                "aired_episodes": int,
                "rating": float,
                "votes": int,
                "comment_count": int,
            },
            pk="id",
            not_null={"id", "season", "number", "trakt_id", "show_id"},
            defaults={"type": "episode"},
        )
        self.db.add_foreign_keys(
            [
                ("extended_episode", "show_id", "extended_show", "id"),
            ]
        )

    def create_extended_movie(self):
        self.db["extended_movie"].create(  # type: ignore
            {
                "type": str,
                "id": int,
                "title": str,
                "year": int,
                "trakt_id": int,
                "trakt_slug": int,
                "imdb_id": str,
                "tmdb_id": int,
                "tagline": str,
                "overview": str,
                "released": str,
                "runtime": int,
                "country": str,
                "trailer": str,
                "homepage": str,
                "status": str,
                "rating": float,
                "votes": int,
                "comment_count": int,
                "language": str,
                "certification": str,
            },
            pk="id",
            not_null={"id", "title", "trakt_id"},
            defaults={"type": "movie"},
        )

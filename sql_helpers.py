from sqlite_utils import Database


class Datastore:
    def __init__(self, db: Database) -> None:
        self.db = db

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

    def create_episode_watchlog(self):
        self.db["episode_watchlog"].create(  # type: ignore
            {
                "id": int,
                "episode_id": int,
                "watched_at": str,
            },
            pk="id",
            not_null={"id", "episode_id", "watched_at"},
            foreign_keys=["episode_id"],
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

    def create_movie_watchlog(self):
        self.db["movie_watchlog"].create(  # type: ignore
            {
                "id": int,
                "movie_id": int,
                "watched_at": str,
            },
            pk="id",
            not_null={"id", "movie_id", "watched_at"},
            foreign_keys=["movie_id"],
        )

    def create_watchlog(self):
        self.db["watchlog"].create(  # type: ignore
            {
                "id": int,
                "type": str,  # movie / episode
                "media_id": int,
                "watched_at": str,
            },
            pk="id",
            not_null={"id", "media_id", "watched_at"},
            # foreign_keys=["media_id"],
        )

        self.db.add_foreign_keys(
            [("watchlog", "media_id", "movie", "id"), ("watchlog", "media_id", "episode", "id")]
        )

    def create_collected(self):
        self.db["collected"].create(  # type: ignore
            {
                "id": str,
                "type": str,  # movie / episode
                "media_id": int,
                "collected_at": str,
            },
            pk="id",
            not_null={"id", "media_id", "collected_at"},
            # foreign_keys=["media_id"],
        )

        self.db.add_foreign_keys(
            [("collected", "media_id", "movie", "id"), ("collected", "media_id", "episode", "id")]
        )

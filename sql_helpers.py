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

    def assert_tables(self) -> bool:
        required_tables = ["show", "episode", "movie", "watchlog", "collected", "ratings"]
        return all([True if table in self.db.table_names() else False for table in required_tables])

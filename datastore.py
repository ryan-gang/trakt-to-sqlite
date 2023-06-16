import json


class Datastore:
    def __init__(self, table_name, db_path=r".\trakt.db") -> None:
        self.db_path = db_path
        self.table_name = table_name

    @staticmethod
    def parse_scrobble_data_history_episodes(item) -> dict[str, str]:
        d = {}
        d["id"] = item["id"]
        d["watched_at"] = item["watched_at"]
        d["action"] = item["action"]
        d["type"] = item["type"]
        d["episode_season"] = item["episode"]["season"]
        d["episode_number"] = item["episode"]["number"]
        d["episode_title"] = item["episode"]["title"]
        d["episode_id_trakt"] = item["episode"]["ids"]["trakt"]
        d["episode_id_imdb"] = item["episode"]["ids"]["imdb"]
        d["show_title"] = item["show"]["title"]
        d["show_year"] = item["show"]["year"]
        d["show_id_trakt"] = item["show"]["ids"]["trakt"]
        d["show_id_imdb"] = item["show"]["ids"]["imdb"]

        return d

    @staticmethod
    def parse_scrobble_data_history_movies(item) -> dict[str, str]:
        d = {}
        d["id"] = item["id"]
        d["watched_at"] = item["watched_at"]
        d["action"] = item["action"]
        d["type"] = item["type"]
        d["movie_title"] = item["movie"]["title"]
        d["movie_year"] = item["movie"]["year"]
        d["movie_id_trakt"] = item["movie"]["ids"]["trakt"]
        d["movie_id_imdb"] = item["movie"]["ids"]["imdb"]
        d["movie_id_slug"] = item["movie"]["ids"]["slug"]
        d["movie_id_tmdb"] = item["movie"]["ids"]["tmdb"]

        return d

    def make_connection(self) -> sqlite3.Connection:
        # Connect to the database
        conn = sqlite3.connect(self.db_path)

        # Create a cursor
        cur = conn.cursor()

        # Check if the table exists
        cur.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table_name}'"
        )
        existing_table = cur.fetchone()

        if not existing_table:
            conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    "id" BIGINT PRIMARY KEY,
                    "watched_at" TEXT,
                    "action" TEXT,
                    "type" TEXT,
                    "episode_season" TEXT,
                    "episode_number" TEXT,
                    "episode_title" TEXT,
                    "episode_id_trakt" TEXT,
                    "episode_id_imdb" TEXT,
                    "show_title" TEXT,
                    "show_year" TEXT,
                    "show_id_trakt" TEXT,
                    "show_id_imdb" TEXT,
                    "movie_title" TEXT,
                    "movie_year" TEXT,
                    "movie_id_trakt" TEXT,
                    "movie_id_imdb" TEXT,
                    "movie_id_slug" TEXT,
                    "movie_id_tmdb" TEXT
                )
                """
            )
        return conn

    def write_multiple_scrobble_data(self, conn, scrobbles, count=0):
        for i in range(len(scrobbles)):
            data = scrobbles[i]
            if data["type"] == "episode":
                d = Datastore.parse_scrobble_data_history_episodes(data)
            elif data["type"] == "movie":
                d = Datastore.parse_scrobble_data_history_movies(data)
            try:
                status = self.write_scrobble_data(conn, d, count)
                count += int(status)
            except sqlite3.IntegrityError:
                print("Duplicate record found. Exiting.")
                break
        conn.commit()

        return count

    def close_connection(self, conn):
        # Commit the changes
        conn.commit()

        # Close the connection
        conn.close()

    def write_scrobble_data(self, conn, item, count) -> None:
        conn.execute(
            f"""
            INSERT INTO {self.table_name}
            (id, watched_at, action, type, episode_season, episode_number, episode_title, episode_id_trakt, episode_id_imdb, show_title, show_year, show_id_trakt, show_id_imdb)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item["id"],
                item["watched_at"],
                item["action"],
                item["type"],
                item["episode_season"],
                item["episode_number"],
                item["episode_title"],
                item["episode_id_trakt"],
                item["episode_id_imdb"],
                item["show_title"],
                item["show_year"],
                item["show_id_trakt"],
                item["show_id_imdb"],
            ),
        )
        print(
            f"{count}. Processed {item['show_title']},"
            f" S{item['episode_season']}E{item['episode_number']}"
        )
        return True


if __name__ == "__main__":
    file = r".\backup\history_movies.json"
    THRESHOLD = int(1000) // 10  # If 10% of records fail to write to disk, return.
    with open(file, "r") as f:
        data = json.load(f)

    store = Datastore(table_name)
    conn = store.make_connection()
    count = store.write_multiple_scrobble_data(conn, data, count=0)

    store.close_connection(conn)

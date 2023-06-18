import argparse
import os

from sqlite_utils import Database

from api import TraktRequest
from core import save_collections_files, save_history_files, save_ratings_files
from parse import Collected, Commons
from sql_helpers import Datastore

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="trakt-to-sqlite")
    parser.add_argument(
        "username",
        help="Pass the trakt username, for backing up data.",
    )
    parser.add_argument(
        "path",
        help=(
            "Pass the location where the backed up files will be stored, and the sqlite database"
            " created."
        ),
    )
    parser.add_argument(
        "--resume",
        "-r",
        action="store_true",
        help=(
            "If backed up files are already present, and it needs to be only ingested into the db."
        ),
    )
    parser.add_argument(
        "--keep",
        "-k",
        action="store_true",
        help="If backed up files are to be stored, by default they will be deleted.",
    )
    parser.add_argument(
        "--nodb",
        "-no",
        action="store_true",
        help="If backed up files are NOT to be ingested to db, by default they will be ingested.",
    )

    args = parser.parse_args()
    if PATH := args.backuppath:
        if not os.path.isdir(PATH):
            os.makedirs(PATH)
    username = args.username
    db_path = os.path.join(PATH, f"{username}.db")
    db: Database = Database(db_path)

    ds = Datastore(db)
    ds.assert_tables()

    cl = Collected()
    c = Commons()
    api = TraktRequest(username, backup_path=PATH)
    api.test_connection()
    api.test_connection()
    api.backup()  # Always pull a backup ?

    # Actual saving to sqlite part.
    save_history_files(db, PATH)
    save_collections_files(db, PATH, api)
    save_ratings_files(db, PATH)

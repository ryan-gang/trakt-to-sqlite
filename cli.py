import argparse
import logging
import os
import time
from datetime import datetime

from sqlite_utils import Database

from api import TraktRequest
from core import (
    save_collections_files,
    save_history_files,
    save_ratings_files,
    save_watchlist_files,
)
from sql_helpers import Datastore

logging.basicConfig()

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
    logger = logging.getLogger("cli")
    logger.setLevel(logging.INFO)
    logger.info(args)
    username, backup_dir = args.username, args.path
    resume_db_ingestion, keep_downloaded_files, ingestion_into_db = (
        args.resume,
        args.keep,
        args.nodb,
    )

    db_exists = False
    start_time = time.time()
    timestamp = datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H%M%S")
    backup_sub_dir = f"backup\\{username}\\{timestamp}"
    backup_path = os.path.join(backup_dir, backup_sub_dir)
    os.makedirs(backup_path, exist_ok=True)

    db_sub_dir = f"backup\\{username}\\{username}.db"
    db_path = os.path.join(backup_dir, db_sub_dir)
    logger.info(f"Backup path : {backup_path}, Database path : {db_path}.")
    if os.path.isfile(db_path):
        db_exists = True

    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    db: Database = Database(db_path)

    ds = Datastore(db)
    if not ds.assert_tables():
        logger.info("All required tables not present. Creating tables.")
        ds.create_tables()

    api = TraktRequest(username, backup_path=backup_path)
    api.test_connection()
    if not resume_db_ingestion:
        logger.info("Polling trakt API to backup user data.")
        api.backup()

    if not ingestion_into_db:
        # Actual saving to sqlite part.
        logger.info("Writing Watchlog to db.")
        save_history_files(db, backup_path)
        logger.info("Writing Collections to db.")
        save_collections_files(db, backup_path, api)
        logger.info("Writing Ratings to db.")
        save_ratings_files(db, backup_path)
        logger.info("Writing Watchlist to db.")
        save_watchlist_files(db, backup_path)
    if not keep_downloaded_files:
        logger.info(f"Deleting all downloaded json files from : {backup_path}")
        os.rmdir(backup_path)
    end_time = time.time()
    print(f"Operation finished in {round(end_time - start_time, 2)} seconds.")

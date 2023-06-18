import os
import json
from typing import Any

from sqlite_utils import Database


def load_json(file_path: str) -> Any:
    assert os.path.isfile(file_path)
    with open(file_path, "r") as f:
        data = json.load(f)
    return data


def get_genre_cache(db: Database) -> dict[str, str]:
    d: dict[str, str] = {}  # genre - genre_id mapping.
    for row in db["genre"].rows:  # type: ignore
        name, id = row["name"], row["id"]  # type: ignore
        d[name] = id  # type: ignore
    return d

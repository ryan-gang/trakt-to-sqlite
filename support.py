import os
import json
from typing import Any


def load_json(file_path: str) -> Any:
    assert os.path.isfile(file_path)
    with open(file_path, "r") as f:
        data = json.load(f)
    return data

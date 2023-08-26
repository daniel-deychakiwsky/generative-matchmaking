import json
import os

from ..data.types import JsonType


def read_json(file_path: str) -> JsonType:
    with open(file_path) as json_file:
        json_obj: JsonType = json.load(json_file)
        return json_obj


def write_json(data: JsonType, file_path: str) -> None:
    directory: str = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok=True)
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

import json
import os
from dataclasses import asdict

from ..data.schemas import UserProfile


def read_user_profile_from_json(file_path: str) -> UserProfile:
    with open(file_path) as json_file:
        return UserProfile(**json.load(json_file))


def write_user_profile_as_json(user_profile: UserProfile, file_path: str) -> None:
    directory: str = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok=True)
    with open(file_path, "w") as json_file:
        json.dump(asdict(user_profile), json_file, indent=4)


def write_user_profile_image_bytes(image_bytes: bytes, file_path: str) -> None:
    with open(file_path, "wb") as fh:
        fh.write(image_bytes)

import json
import os
from dataclasses import asdict

from ..data.schemas import UserProfile


def read_user_profile_from_json(file_path: str) -> UserProfile:
    with open(file_path) as json_file:
        json_obj: UserProfile = UserProfile(**json.load(json_file))
        return json_obj


def write_user_profile_as_json(user_profile: UserProfile, file_path: str) -> None:
    directory: str = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok=True)
    with open(file_path, "w") as json_file:
        json.dump(asdict(user_profile), json_file, indent=4)

import json
import os
import typing
from dataclasses import asdict
from typing import Dict, List

from ..data.types import JSON
from ..data.user_profile import UserProfile, user_profile_from_json
from .constants import (
    USER_PROFILE_FILE_NAME,
    USER_PROFILE_IMAGE_FILE_NAME,
    USER_PROFILE_MATCHES_FILE_NAME,
    USER_PROFILE_SUB_DIRECTORY,
)


def _user_profile_files_exists(user_id: str, file: str) -> bool:
    return os.path.isfile(os.path.join(USER_PROFILE_SUB_DIRECTORY, user_id, file))


def read_all_user_profiles() -> List[UserProfile]:
    return [
        read_user_profile(user_id=user_id)
        for user_id in os.listdir(USER_PROFILE_SUB_DIRECTORY)
        if os.path.isdir(os.path.join(USER_PROFILE_SUB_DIRECTORY, user_id))
    ]


@typing.no_type_check
def read_user_profile(user_id: str) -> UserProfile:
    file_path: str = os.path.join(
        USER_PROFILE_SUB_DIRECTORY,
        user_id,
        USER_PROFILE_FILE_NAME,
    )
    return user_profile_from_json(user_profile_json=read_json(file_path=file_path))


def write_user_profile(user_profile: UserProfile) -> None:
    file_path: str = os.path.join(
        USER_PROFILE_SUB_DIRECTORY,
        user_profile.user_id,
        USER_PROFILE_FILE_NAME,
    )
    directory: str = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok=True)
    with open(file_path, "w") as json_file:
        json.dump(asdict(user_profile), json_file, indent=4)


def write_user_profile_matches(
    user_profile: UserProfile, matches: Dict[str, List[str]]
) -> None:
    file_path: str = os.path.join(
        USER_PROFILE_SUB_DIRECTORY,
        user_profile.user_id,
        USER_PROFILE_MATCHES_FILE_NAME,
    )
    directory: str = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok=True)
    with open(file_path, "w") as json_file:
        json.dump(matches, json_file, indent=4)


def write_user_profile_image(user_id: str, image_bytes: bytes) -> None:
    file_path: str = os.path.join(
        USER_PROFILE_SUB_DIRECTORY,
        user_id,
        USER_PROFILE_IMAGE_FILE_NAME,
    )
    with open(file_path, "wb") as fh:
        fh.write(image_bytes)


@typing.no_type_check
def read_json(file_path: str) -> JSON:
    with open(file_path) as json_file:
        return json.load(json_file)

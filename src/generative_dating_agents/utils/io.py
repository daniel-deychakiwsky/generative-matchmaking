import json
import os
from dataclasses import asdict
from typing import Dict, List

from ..data.schemas import UserProfile

DEFAULT_USER_PROFILE_SUB_DIRECTORY: str = os.path.join(os.getcwd(), "profiles")
DEFAULT_USER_PROFILE_FILE_NAME: str = "profile.json"
DEFAULT_USER_PROFILE_MATCHES_FILE_NAME: str = "matches.json"
DEFAULT_USER_PROFILE_IMAGE_FILE_NAME: str = "profile.png"


def _user_profile_files_exists(user_id: str, file: str) -> bool:
    return os.path.isfile(
        os.path.join(DEFAULT_USER_PROFILE_SUB_DIRECTORY, user_id, file)
    )


def read_all_user_profiles(
    with_missing_profile: bool = False,
    with_missing_image: bool = False,
    with_missing_matches: bool = False,
) -> List[UserProfile]:
    missing_files: List[str] = []

    if with_missing_profile:
        missing_files.append(DEFAULT_USER_PROFILE_FILE_NAME)

    if with_missing_image:
        missing_files.append(DEFAULT_USER_PROFILE_IMAGE_FILE_NAME)

    if with_missing_matches:
        missing_files.append(DEFAULT_USER_PROFILE_MATCHES_FILE_NAME)

    return [
        read_user_profile(user_id=user_id)
        for user_id in os.listdir(DEFAULT_USER_PROFILE_SUB_DIRECTORY)
        if os.path.isdir(os.path.join(DEFAULT_USER_PROFILE_SUB_DIRECTORY, user_id))
        and not any(
            _user_profile_files_exists(user_id=user_id, file=file)
            for file in missing_files
        )
    ]


def read_user_profile(user_id: str) -> UserProfile:
    file_path: str = os.path.join(
        DEFAULT_USER_PROFILE_SUB_DIRECTORY,
        user_id,
        DEFAULT_USER_PROFILE_FILE_NAME,
    )
    with open(file_path) as json_file:
        return UserProfile(**json.load(json_file))


def write_user_profile(user_profile: UserProfile) -> None:
    file_path: str = os.path.join(
        DEFAULT_USER_PROFILE_SUB_DIRECTORY,
        user_profile.user_id,
        DEFAULT_USER_PROFILE_FILE_NAME,
    )
    directory: str = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok=True)
    with open(file_path, "w") as json_file:
        json.dump(asdict(user_profile), json_file, indent=4)


def write_user_profile_matches(
    user_profile: UserProfile, matches: Dict[str, List[str]]
) -> None:
    file_path: str = os.path.join(
        DEFAULT_USER_PROFILE_SUB_DIRECTORY,
        user_profile.user_id,
        DEFAULT_USER_PROFILE_MATCHES_FILE_NAME,
    )
    directory: str = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok=True)
    with open(file_path, "w") as json_file:
        json.dump(matches, json_file, indent=4)


def write_user_profile_image(user_id: str, image_bytes: bytes) -> None:
    file_path: str = os.path.join(
        DEFAULT_USER_PROFILE_SUB_DIRECTORY,
        user_id,
        DEFAULT_USER_PROFILE_IMAGE_FILE_NAME,
    )
    with open(file_path, "wb") as fh:
        fh.write(image_bytes)

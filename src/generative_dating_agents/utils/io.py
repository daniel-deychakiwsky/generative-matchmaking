import json
import os
import typing
from dataclasses import asdict
from typing import Dict, List, Tuple

from ..data.models import UserProfile, user_profile_from_json
from .constants import (
    USER_MATCH_RANKED_KEY,
    USER_MATCH_RETRIEVED_KEY,
    USER_PROFILE_FILE_NAME,
    USER_PROFILE_IMAGE_FILE_NAME,
    USER_PROFILE_MATCHES_FILE_NAME,
    USER_PROFILE_SUB_DIRECTORY,
)
from .types import JSON


def _user_profile_files_exists(user_id: str, file: str) -> bool:
    return os.path.isfile(os.path.join(USER_PROFILE_SUB_DIRECTORY, user_id, file))


def read_all_user_profiles(
    with_missing_profile: bool = False,
    with_missing_image: bool = False,
    with_missing_matches: bool = False,
) -> List[UserProfile]:
    missing_files: List[str] = []

    if with_missing_profile:
        missing_files.append(USER_PROFILE_FILE_NAME)

    if with_missing_image:
        missing_files.append(USER_PROFILE_IMAGE_FILE_NAME)

    if with_missing_matches:
        missing_files.append(USER_PROFILE_MATCHES_FILE_NAME)

    return [
        read_user_profile(user_id=user_id)
        for user_id in os.listdir(USER_PROFILE_SUB_DIRECTORY)
        if os.path.isdir(os.path.join(USER_PROFILE_SUB_DIRECTORY, user_id))
        and not any(
            _user_profile_files_exists(user_id=user_id, file=file)
            for file in missing_files
        )
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


@typing.no_type_check
def read_user_matches(
    user_id: str, verbose: bool = True
) -> Tuple[UserProfile, List[UserProfile], List[UserProfile]]:
    user_matches_file_path: str = os.path.join(
        USER_PROFILE_SUB_DIRECTORY,
        user_id,
        USER_PROFILE_MATCHES_FILE_NAME,
    )
    query_user_profile: UserProfile = read_user_profile(user_id=user_id)
    user_id_matches_json: JSON = read_json(file_path=user_matches_file_path)
    user_profile_matches_retrievals: List[UserProfile] = []
    user_profile_matches_rankings: List[UserProfile] = []

    if USER_MATCH_RETRIEVED_KEY in user_id_matches_json:
        for user_id in user_id_matches_json[USER_MATCH_RETRIEVED_KEY]:
            user_profile_matches_retrievals.append(read_user_profile(user_id=user_id))

    if USER_MATCH_RANKED_KEY in user_id_matches_json:
        for user_id in user_id_matches_json[USER_MATCH_RANKED_KEY]:
            user_profile_matches_rankings.append(read_user_profile(user_id=user_id))

    if verbose:
        print()
        print("--" * 50)
        print("Query user")
        print("--" * 50)
        print()
        print(query_user_profile)
        print()
        print("--" * 50)
        print("Ranked user profiles")
        print("--" * 50)
        print()
        for ranked_user_profile in user_profile_matches_rankings:
            print(ranked_user_profile)
            print()

    return (
        query_user_profile,
        user_profile_matches_retrievals,
        user_profile_matches_rankings,
    )

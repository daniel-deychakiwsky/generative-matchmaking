import typing
from dataclasses import dataclass
from typing import Dict, List, Union

JSON = Dict[
    str,
    Union[
        str,
        int,
        float,
        bool,
        None,
        "JSON",
        List[Union[str, int, float, bool, None, "JSON"]],
    ],
]


# TODO: clean inputs, e.g., .strip()
@dataclass
class PartnerPreferences:
    minimum_age: int
    maximum_age: int
    minimum_height: str
    maximum_height: str
    has_children: bool
    want_children: bool
    sexuality: str
    drinking: str
    smoking: str
    marijuana: str
    drugs: str
    exercise: str
    gender: str
    dating_intentions: str
    relationship_type: str
    ethnicities: List[str]
    politics: List[str]
    job_industry: List[str]
    languages_spoken: List[str]
    values: List[str]
    interests: List[str]
    education_level: List[str]


# TODO: clean inputs, e.g., .strip()
@dataclass
class UserProfile:
    name: str
    age: int
    height: str
    school: str
    job_industry: str
    job_title: str
    hometown_location: str
    dating_location: str
    languages_spoken: List[str]
    values: List[str]
    interests: List[str]
    education_level: str
    religious_beliefs: str
    politics: str
    dating_intentions: str
    relationship_type: str
    gender: str
    pronouns: str
    sexuality: str
    ethnicity: str
    has_children: bool
    want_children: bool
    pets: List[str]
    zodiac_sign: str
    mbti_personality_type: str
    drinking: str
    smoking: str
    marijuana: str
    drugs: str
    exercise: str
    partner_preferences: PartnerPreferences
    profile_summary: str
    preferences_summary: str
    user_id: str


@typing.no_type_check
def user_profile_from_json(user_profile_json: JSON) -> UserProfile:
    return UserProfile(**user_profile_json)

from typing import Dict, List

from ..data.user_profile import UserProfile
from ..database.ops import QueryResult, query_user_profile_collection
from ..utils.constants import MATCHES_KEY
from ..utils.io import (
    read_all_user_profiles,
    read_user_profile,
    write_user_profile_matches,
)


def _retrieve_candidate_user_profiles(
    query_user_profile: UserProfile, n_retrievals: int
) -> List[UserProfile]:
    query_result: QueryResult = query_user_profile_collection(
        query_texts=query_user_profile.preferences_summary,
        n_results=n_retrievals,
        where={
            "$and": [
                {"gender": {"$eq": query_user_profile.partner_preferences.gender}},
                {
                    "sexuality": {
                        "$eq": query_user_profile.partner_preferences.sexuality
                    }
                },
            ]
        },
    )

    return [
        read_user_profile(user_id=user_id)
        for user_id in (query_result["ids"][0] if len(query_result["ids"]) else [])
    ]


def find_matches(user_id: str, n_matches: int) -> Dict[str, List[str]]:
    query_user_profile: UserProfile = read_user_profile(user_id=user_id)
    candidate_user_profiles: List[UserProfile] = _retrieve_candidate_user_profiles(
        query_user_profile=query_user_profile, n_retrievals=n_matches
    )
    candidate_user_ids: List[str] = [p.user_id for p in candidate_user_profiles]
    matches: Dict[str, List[str]] = {MATCHES_KEY: candidate_user_ids}
    write_user_profile_matches(user_profile=query_user_profile, matches=matches)

    return matches


def find_matches_for_all(n_matches: int) -> None:
    user_profiles: List[UserProfile] = read_all_user_profiles()
    for user_profile in user_profiles:
        find_matches(user_id=user_profile.user_id, n_matches=n_matches)

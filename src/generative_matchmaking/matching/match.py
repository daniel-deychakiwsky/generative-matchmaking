from typing import Dict, List, Tuple

from ..data.user_profile import UserProfile
from ..database.ops import QueryResult, query_user_profile_collection
from ..utils.constants import BIDIRECTIONAL_MATCH, UNIDIRECTIONAL_MATCH
from ..utils.io import (
    read_all_user_profiles,
    read_user_profile,
    write_user_profile_matches,
)


def _retrieve_candidate_user_profiles(
    query_user_profile: UserProfile, n_retrievals: int
) -> List[Tuple[UserProfile, float]]:
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

    candidate_user_profiles = [
        read_user_profile(user_id=user_id)
        for user_id in (query_result["ids"][0] if len(query_result["ids"]) else [])
    ]
    candidate_distances = (
        (query_result["distances"][0] if len(query_result["distances"]) else [])
        if query_result["distances"]
        else []
    )

    return list(zip(candidate_user_profiles, candidate_distances))


def find_matches(user_id: str, n_matches: int) -> Dict[str, List[str]]:
    query_user_profile: UserProfile = read_user_profile(user_id=user_id)

    candidates: List[Tuple[UserProfile, float]] = _retrieve_candidate_user_profiles(
        query_user_profile=query_user_profile, n_retrievals=n_matches
    )

    candidate_candidates: Dict[str, Dict[str, float]] = {
        candidate_user_profile.user_id: {
            c_candidate_user_profile.user_id: c_candidate_distance * candidate_distance
            for c_candidate_user_profile, c_candidate_distance in _retrieve_candidate_user_profiles(
                query_user_profile=candidate_user_profile, n_retrievals=n_matches
            )
        }
        for candidate_user_profile, candidate_distance in candidates
    }

    bidirectional_candidate_user_ids: List[str] = [
        item[0]
        for item in sorted(
            {
                candidate_user_profile_id: c_candidate_dict[query_user_profile.user_id]
                for candidate_user_profile_id, c_candidate_dict in candidate_candidates.items()
                if query_user_profile.user_id in c_candidate_dict
            }.items(),
            key=lambda x: x[1],
        )
    ]

    unidirectional_candidate_user_ids: List[str] = [
        candidate_user_profile.user_id
        for candidate_user_profile, _ in candidates
        if candidate_user_profile.user_id not in bidirectional_candidate_user_ids
    ]

    matches: Dict[str, List[str]] = {
        UNIDIRECTIONAL_MATCH: unidirectional_candidate_user_ids,
        BIDIRECTIONAL_MATCH: bidirectional_candidate_user_ids,
    }
    write_user_profile_matches(user_profile=query_user_profile, matches=matches)

    return matches


def find_matches_for_all(n_matches: int) -> None:
    user_profiles: List[UserProfile] = read_all_user_profiles()
    for user_profile in user_profiles:
        find_matches(user_id=user_profile.user_id, n_matches=n_matches)

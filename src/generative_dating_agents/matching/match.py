import json
from typing import Collection, Dict, List

from ..data.schemas import UserProfile
from ..database.chroma import QueryResult, query_user_profile_collection
from ..llm.oai import Conversation, chat_completion
from ..utils.io import read_user_profile
from .schemas import most_compatible_user_id_schema


class MatchingError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(f"MatchingError: {message}")


def _retrieve_candidate_user_profiles(
    query_user_profile: UserProfile, num_retrievals: int
) -> List[UserProfile]:
    query_result: QueryResult = query_user_profile_collection(
        query_texts=query_user_profile.preferences_summary,
        n_results=num_retrievals,
    )

    return [
        read_user_profile(user_id=user_id)
        for user_id in (query_result["ids"][0] if len(query_result["ids"]) else [])
    ]


def _extract_user_description(user_profile: UserProfile) -> str:
    return (
        user_profile.profile_summary.strip()
        + " "
        + user_profile.preferences_summary.strip()
    )


def _build_ranking_system_prompt(query_user_profile: UserProfile) -> str:
    return (
        "You are an expert dating matchmaker.\n\nAssume the identity of the following user and think like they would.\n\n"
        + _extract_user_description(user_profile=query_user_profile)
    )


def _build_ranking_prompt(candidate_user_descriptions: Dict[str, str]) -> str:
    return (
        "Pick one user that you think is most compatible with you. Think step-by-step and explain why. Output the corresponding user id.\n\n"
        + "\n\n".join([k + ": " + v for k, v in candidate_user_descriptions.items()])
    )


def _rank_candidate_user_profiles(
    query_user_profile: UserProfile,
    candidate_user_profiles: List[UserProfile],
    num_matches: int,
) -> List[UserProfile]:
    ranked_candidate_user_ids: List[str] = []

    ranking_system_prompt: str = _build_ranking_system_prompt(
        query_user_profile=query_user_profile
    )

    candidate_user_descriptions: Dict[str, str] = {
        candidate_user_profile.user_id: _extract_user_description(
            candidate_user_profile
        )
        for candidate_user_profile in candidate_user_profiles
    }

    for _ in range(num_matches):
        ranking_prompt: str = _build_ranking_prompt(
            candidate_user_descriptions=candidate_user_descriptions
        )

        function_name: str = "set_most_compatible_user_id"
        functions: list[dict[str, Collection[str]]] = [
            {"name": function_name, "parameters": most_compatible_user_id_schema}
        ]
        function_call: Dict[str, str] = {"name": function_name}

        conversation: Conversation = Conversation()
        conversation.add_system_message(message=ranking_system_prompt)
        conversation.add_user_message(message=ranking_prompt)
        messages: List[Dict[str, str]] = conversation.get_messages()

        most_compatible_user_id_json_str: str = chat_completion(
            model="gpt-3.5-turbo-16k-0613",
            messages=messages,
            temperature=0.0,
            max_tokens=5000,
            functions=functions,
            function_call=function_call,
        )

        most_compatible_user_id: str = json.loads(most_compatible_user_id_json_str)[
            "user_id"
        ]
        candidate_user_descriptions.pop(most_compatible_user_id)
        ranked_candidate_user_ids.append(most_compatible_user_id)

    return [read_user_profile(user_id=user_id) for user_id in ranked_candidate_user_ids]


def find_matches(
    user_id: str, num_retrievals: int, num_matches: int
) -> List[UserProfile]:
    if num_matches > num_retrievals:
        raise MatchingError("invalid")

    query_user_profile: UserProfile = read_user_profile(user_id=user_id)

    candidate_user_profiles: List[UserProfile] = _retrieve_candidate_user_profiles(
        query_user_profile=query_user_profile, num_retrievals=num_retrievals
    )

    adjusted_num_matches: int = min(num_matches, len(candidate_user_profiles))
    ranked_candidate_user_profiles: List[UserProfile] = _rank_candidate_user_profiles(
        query_user_profile=query_user_profile,
        candidate_user_profiles=candidate_user_profiles,
        num_matches=adjusted_num_matches,
    )

    print(ranked_candidate_user_profiles)

    return ranked_candidate_user_profiles


find_matches(
    user_id="f0e35556-8760-41ae-b0f9-4c777c48b170", num_retrievals=20, num_matches=5
)

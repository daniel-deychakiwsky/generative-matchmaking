import json
import time
from typing import Collection, Dict, List

from ..data.schemas import UserProfile
from ..database.chroma import QueryResult, query_user_profile_collection
from ..llm.oai import Conversation, chat_completion
from ..utils.io import (
    read_all_user_profiles,
    read_user_profile,
    write_user_profile_matches,
)
from ..utils.types import JSON
from .schemas import most_compatible_user_id_schema

DEFAULT_OPENAI_RATE_LIMIT_SLEEP_SECONDS: int = 10


class MatchingError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(f"MatchingError: {message}")


def _retrieve_candidate_user_profiles(
    query_user_profile: UserProfile, n_retrievals: int
) -> List[UserProfile]:
    query_result: QueryResult = query_user_profile_collection(
        query_texts=query_user_profile.preferences_summary,
        n_results=n_retrievals,
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
    n_matches: int,
    model: str,
    temperature: float,
    max_tokens: int,
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

    for _ in range(n_matches):
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
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            functions=functions,
            function_call=function_call,
        )

        most_compatible_user_id_json: JSON = json.loads(
            most_compatible_user_id_json_str
        )

        if "user_id" in most_compatible_user_id_json:
            most_compatible_user_id: str = most_compatible_user_id_json["user_id"]  # type: ignore

            if most_compatible_user_id in candidate_user_descriptions:
                candidate_user_descriptions.pop(most_compatible_user_id)
                ranked_candidate_user_ids.append(most_compatible_user_id)
            else:
                print(
                    "Hallucinated candidate user_id key for user:",
                    query_user_profile.user_id,
                )
        else:
            print(
                "Missing candidate user_id JSON key for user:",
                query_user_profile.user_id,
            )

    return [read_user_profile(user_id=user_id) for user_id in ranked_candidate_user_ids]


def find_matches(
    user_id: str,
    n_retrievals: int,
    n_matches: int,
    model: str,
    temperature: float,
    max_tokens: int,
    verbose: bool,
) -> Dict[str, List[str]]:
    if n_matches > n_retrievals:
        raise MatchingError("invalid")

    query_user_profile: UserProfile = read_user_profile(user_id=user_id)
    retrieved_candidate_user_profiles: List[
        UserProfile
    ] = _retrieve_candidate_user_profiles(
        query_user_profile=query_user_profile, n_retrievals=n_retrievals
    )
    ranked_candidate_user_profiles: List[UserProfile] = _rank_candidate_user_profiles(
        query_user_profile=query_user_profile,
        candidate_user_profiles=retrieved_candidate_user_profiles,
        n_matches=min(n_matches, len(retrieved_candidate_user_profiles)),
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    if verbose:
        print()
        print("--" * 50)
        print("Query user")
        print("--" * 50)
        print()
        print(query_user_profile)
        print()
        print("--" * 50)
        print("Retrieved candidates")
        print("--" * 50)
        print()
        for retrieved_user_profile in retrieved_candidate_user_profiles:
            print(retrieved_user_profile)
            print()
        print("--" * 50)
        print("Ranked candidates")
        print("--" * 50)
        print()
        for ranked_user_profile in ranked_candidate_user_profiles:
            print(ranked_user_profile)
            print()

    matches: Dict[str, List[str]] = {
        "retrieved": [p.user_id for p in retrieved_candidate_user_profiles],
        "ranked": [p.user_id for p in ranked_candidate_user_profiles],
    }

    write_user_profile_matches(user_profile=query_user_profile, matches=matches)

    return matches


def find_matches_for_all(
    n_retrievals: int,
    n_matches: int,
    model: str,
    temperature: float,
    max_tokens: int,
    verbose: bool,
) -> None:
    # run for user profiles without matches to not overwrite existing
    with_missing_matches: bool = True
    user_profiles: List[UserProfile] = read_all_user_profiles(
        with_missing_matches=with_missing_matches
    )
    for user_profile in user_profiles:
        find_matches(
            user_id=user_profile.user_id,
            n_retrievals=n_retrievals,
            n_matches=n_matches,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            verbose=verbose,
        )
        time.sleep(DEFAULT_OPENAI_RATE_LIMIT_SLEEP_SECONDS)

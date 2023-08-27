import copy
import json
import os
import random
import uuid
from typing import Collection, Dict, List, Tuple

from ..llm.oai import Conversation, chat_completion, text_to_image
from ..utils.io import write_user_profile_as_json, write_user_profile_image_bytes
from ..utils.types import JSON
from .schemas import UserProfile, user_profile_function_schema

SYSTEM_PROMPT: str = "You are a helpful assistant."


def _generate_user_profile(
    model: str,
    max_tokens: int,
    temperature: float,
) -> JSON:
    prompt_sfx: str = "Ensure balanced diversity."
    prompt_one: str = "Generate 10 unique first and last names."

    if random.choice([0, 1]):
        prompt_one += " " + prompt_sfx

    conversation: Conversation = Conversation()
    conversation.add_system_message(message=SYSTEM_PROMPT)
    conversation.add_user_message(message=prompt_one)

    messages_instruct_generate_user_names: List[
        Dict[str, str]
    ] = conversation.get_messages()

    user_profile_names: str = chat_completion(
        model=model,
        messages=messages_instruct_generate_user_names,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    prompt_two: str = "Choose a name randomly and generate a dating profile for them."

    if random.choice([0, 1]):
        prompt_two += " " + prompt_sfx

    function_name: str = "set_dating_profile"
    functions: list[dict[str, Collection[str]]] = [
        {"name": function_name, "parameters": user_profile_function_schema}
    ]
    function_call: Dict[str, str] = {"name": function_name}

    conversation.add_assistant_message(message=user_profile_names)
    conversation.add_user_message(message=prompt_two)

    messages_instruct_generate_dating_profile: List[
        Dict[str, str]
    ] = conversation.get_messages()

    user_dating_profile_json_str: str = chat_completion(
        model=model,
        messages=messages_instruct_generate_dating_profile,
        max_tokens=max_tokens,
        temperature=temperature,
        functions=functions,
        function_call=function_call,
    )

    user_profile_json: JSON = json.loads(user_dating_profile_json_str)

    return user_profile_json


def _generate_user_summary(
    user_profile_json: JSON,
    prompt: str,
    model: str,
    max_tokens: int,
    temperature: float,
) -> str:
    user_profile_json_copy: JSON = copy.deepcopy(user_profile_json)
    user_profile_json_copy.pop("name")
    user_profile_json_copy_str: str = json.dumps(user_profile_json_copy, indent=4)

    conversation: Conversation = Conversation()
    conversation.add_system_message(message=SYSTEM_PROMPT)
    conversation.add_user_message(message=user_profile_json_copy_str + "\n\n" + prompt)

    messages_instruct_summarize: List[Dict[str, str]] = conversation.get_messages()

    summary: str = chat_completion(
        model=model,
        messages=messages_instruct_summarize,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    return summary


def _generate_user_profile_summaries(
    user_profile_json: JSON,
    model: str,
    max_tokens: int,
    temperature: float,
) -> Tuple[str, str]:
    prompt_sum_profile: str = "Summarize the user's dating profile.\nInclude all fields other than partner_preferences.\nOutput a concise paragraph."
    prompt_sum_preferences: str = "Summarize the user's dating partner_preferences.\nInclude partner_preferences fields only and nothing else.\nOutput a concise paragraph."

    user_profile_summary: str = _generate_user_summary(
        user_profile_json=user_profile_json,
        prompt=prompt_sum_profile,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    user_preferences_summary: str = _generate_user_summary(
        user_profile_json=user_profile_json,
        prompt=prompt_sum_preferences,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    return user_profile_summary, user_preferences_summary


def _generate_user_profile_image(user_profile: UserProfile) -> bytes:
    prompt: str = (
        f"Dating profile picture of a "
        f"{user_profile.height} {user_profile.ethnicity} {user_profile.age} "
        f"year old {user_profile.gender} ({user_profile.pronouns}) "
        f"with an {user_profile.exercise} physique who works as a "
        f"{user_profile.job_industry} professional "
        f"that values {' and '.join(user_profile.values[:2])} "
        f"who enjoys {' and '.join(user_profile.interests[:2])} who "
        f"identifies as {user_profile.religious_beliefs}."
    )

    image_bytes: bytes = text_to_image(prompt=prompt)

    return image_bytes


def generate_profiles(
    num_profiles: int,
    model: str,
    max_tokens: int,
    temperature: float,
    output_directory: str,
    output_file_name: str,
    output_image_file_name: str,
) -> None:
    for _ in range(0, num_profiles):
        user_profile_json: JSON = _generate_user_profile(
            model=model, max_tokens=max_tokens, temperature=temperature
        )
        (
            user_profile_summary,
            user_preferences_summary,
        ) = _generate_user_profile_summaries(
            user_profile_json=user_profile_json,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        user_profile_json["profile_summary"] = user_profile_summary
        user_profile_json["preferences_summary"] = user_preferences_summary
        user_profile_json["user_id"] = str(uuid.uuid4())
        user_profile: UserProfile = UserProfile(**user_profile_json)  # type: ignore[arg-type]

        image_bytes: bytes = _generate_user_profile_image(user_profile=user_profile)

        output_directory_path: str = os.path.join(
            os.getcwd(),
            output_directory,
            user_profile.user_id,
        )
        output_user_profile_file_path = os.path.join(
            output_directory_path, output_file_name
        )
        output_user_profile_image_file_path = os.path.join(
            output_directory_path, output_image_file_name
        )

        write_user_profile_as_json(
            user_profile=user_profile, file_path=output_user_profile_file_path
        )
        write_user_profile_image_bytes(
            image_bytes=image_bytes, file_path=output_user_profile_image_file_path
        )

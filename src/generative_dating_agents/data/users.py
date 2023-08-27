import json
import os
import random
import uuid
from typing import Collection, Dict, List

from joblib import Parallel, delayed

from ..llm.oai import Conversation, chat_completion, text_to_image
from ..utils.io import write_user_profile_as_json, write_user_profile_image_bytes
from ..utils.types import JSON
from .schemas import UserProfile, user_profile_function_schema


def generate_profiles(
    num_profiles: int,
    model: str,
    max_tokens: int,
    temperature: float,
    output_directory: str,
    output_file_name: str,
    output_image_file_name: str,
    n_jobs: int = -1,
) -> None:
    sys_prompt: str = "You are a helpful assistant."
    gen_names_prompt: str = "Generate 10 unique first and last names."
    gen_dating_prompt: str = (
        "Choose a name randomly and generate a dating profile for them."
    )
    sum_dating_prompt: str = "Summarize the user's dating profile.\nInclude all fields other than their partner_preferences.\nDo not output the user's name."
    sum_partner_preferences_prompt: str = "Summarize only the user's dating partner_preferences.\nInclude all of the partner_preferences fields.\nDo not output the user's name."
    stochastic_diversity_suffix: str = "Ensure balanced diversity."
    text_to_image_prompt: str = (
        "Dating profile picture of a "
        "{height} {ethnicity} {age} year old {gender} ({pronouns}) "
        "with an {exercise} physique who works as a {job_industry} professional "
        "that values {values_one} and {values_two} "
        "who enjoys {interests_one} and {interests_two} who "
        "identifies as {religious_beliefs}."
    )

    function_name: str = "set_dating_profile"
    functions: list[dict[str, Collection[str]]] = [
        {"name": function_name, "parameters": user_profile_function_schema}
    ]
    function_call: Dict[str, str] = {"name": function_name}

    def gen() -> UserProfile:
        stochastic_gen_names_prompt = gen_names_prompt
        stochastic_gen_dating_prompt = gen_dating_prompt

        if random.choice([0, 1]):
            stochastic_gen_names_prompt = (
                stochastic_gen_names_prompt + " " + stochastic_diversity_suffix
            )

        if random.choice([0, 1]):
            stochastic_gen_dating_prompt = (
                stochastic_gen_dating_prompt + " " + stochastic_diversity_suffix
            )

        conversation: Conversation = Conversation()
        conversation.add_system_message(message=sys_prompt)
        conversation.add_user_message(message=stochastic_gen_names_prompt)

        messages_instruct_generate_names: List[
            Dict[str, str]
        ] = conversation.get_messages()

        user_profile_names: str = chat_completion(
            model=model,
            messages=messages_instruct_generate_names,
            max_tokens=max_tokens,
            temperature=temperature,
            functions=None,
            function_call=None,
        )

        conversation.add_assistant_message(message=user_profile_names)
        conversation.add_user_message(message=stochastic_gen_dating_prompt)

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

        conversation_two: Conversation = Conversation()
        conversation_two.add_system_message(message=sys_prompt)
        conversation_two.add_user_message(
            message=user_dating_profile_json_str + "\n\n" + sum_dating_prompt
        )

        messages_instruct_summarize_dating_profile: List[
            Dict[str, str]
        ] = conversation_two.get_messages()

        user_profile_summary: str = chat_completion(
            model=model,
            messages=messages_instruct_summarize_dating_profile,
            max_tokens=max_tokens,
            temperature=temperature,
            functions=None,
            function_call=None,
        )

        conversation_three: Conversation = Conversation()
        conversation_three.add_system_message(message=sys_prompt)
        conversation_three.add_user_message(
            message=user_dating_profile_json_str
            + "\n\n"
            + sum_partner_preferences_prompt
        )

        messages_instruct_summarize_partner_preferences: List[
            Dict[str, str]
        ] = conversation_three.get_messages()

        user_partner_preferences_summary: str = chat_completion(
            model=model,
            messages=messages_instruct_summarize_partner_preferences,
            max_tokens=max_tokens,
            temperature=temperature,
            functions=None,
            function_call=None,
        )

        user_profile_json["profile_summary"] = user_profile_summary
        user_profile_json["preferences_summary"] = user_partner_preferences_summary
        user_profile_json["user_id"] = str(uuid.uuid4())

        return UserProfile(**user_profile_json)  # type: ignore[arg-type]

    def parallel_gen() -> List[UserProfile]:
        user_profiles_accum: List[UserProfile] = Parallel(n_jobs=n_jobs)(
            delayed(gen)() for _ in range(num_profiles)
        )
        return user_profiles_accum

    user_profiles: List[UserProfile] = parallel_gen()

    for user_profile in user_profiles:
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

        text_to_image_profile_prompt = text_to_image_prompt.format(
            age=user_profile.age,
            gender=user_profile.gender,
            pronouns=user_profile.pronouns,
            ethnicity=user_profile.ethnicity,
            height=user_profile.height,
            job_industry=user_profile.job_industry,
            exercise=user_profile.exercise,
            values_one=user_profile.values[0],
            values_two=user_profile.values[1],
            interests_one=user_profile.interests[0],
            interests_two=user_profile.interests[1],
            religious_beliefs=user_profile.religious_beliefs,
        )

        image_bytes: bytes = text_to_image(
            prompt=text_to_image_profile_prompt,
        )

        write_user_profile_image_bytes(
            image_bytes=image_bytes, file_path=output_user_profile_image_file_path
        )

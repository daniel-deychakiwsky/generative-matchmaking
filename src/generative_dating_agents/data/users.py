import base64
from openai import Image
import json
import os
import random
import uuid
from typing import Collection, Dict, List

from joblib import Parallel, delayed

from ..llm.oai import Conversation, chat_completion
from ..utils.io import write_user_profile_as_json
from ..utils.types import JSON
from .schemas import UserProfile, user_profile_function_schema


def generate_profiles(
    num_profiles: int,
    model: str,
    max_tokens: int,
    temperature: float,
    output_directory: str,
    output_file_name: str,
    n_jobs: int = -1,
) -> None:
    sys_prompt: str = "You are a helpful assistant."
    gen_names_prompt: str = "Generate 10 unique first and last names."
    gen_dating_prompt: str = (
        "Choose a name randomly and generate a dating profile for them."
    )
    sum_dating_prompt: str = "Summarize the user's dating profile."
    stochastic_diversity_suffix: str = "Ensure balanced diversity."

    function_name: str = "set_dating_profile"
    functions: list[dict[str, Collection[str]]] = [
        {"name": function_name, "parameters": user_profile_function_schema}
    ]
    function_call: Dict[str, str] = {"name": function_name}

    output_filepath: str = os.path.join(
        os.getcwd(), f"{output_filename}.jsonl")

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

        conversation.add_assistant_message(
            message=user_dating_profile_json_str)
        conversation.add_user_message(message=sum_dating_prompt)

        messages_instruct_summarize_dating_profile: List[
            Dict[str, str]
        ] = conversation.get_messages()

        user_profile_summary: str = chat_completion(
            model=model,
            messages=messages_instruct_summarize_dating_profile,
            max_tokens=max_tokens,
            temperature=temperature,
            functions=None,
            function_call=None,
        )

        user_profile_json["summary"] = user_profile_summary
        user_profile_json["user_id"] = str(uuid.uuid4())

        return UserProfile(**user_profile_json)  # type: ignore[arg-type]

    def parallel_gen() -> List[UserProfile]:
        user_profiles_accum: List[UserProfile] = Parallel(n_jobs=n_jobs)(
            delayed(gen)() for _ in range(num_profiles)
        )
        return user_profiles_accum

    user_profiles: List[UserProfile] = parallel_gen()

    for user_profile in user_profiles:
        output_file_path: str = os.path.join(
            os.getcwd(),
            output_directory,
            user_profile.user_id,
            output_file_name,
        )

        write_user_profile_as_json(
            user_profile=user_profile, file_path=output_file_path
        )


def generate_profile_photo_prompt(profile):
    # Extract relevant physical, style, and personality details
    name = profile["name"]
    age = profile["age"]
    height = profile["height"]
    gender = profile["gender"]
    pronouns = profile["pronouns"]
    ethnicity = profile["ethnicity"]
    job_industry = profile["job_industry"]
    exercise = profile["exercise"]
    interests = ", ".join(profile["interests"][:2])
    religious_beliefs = profile["religious_beliefs"]
    # Taking first two values due to length constraints
    values = ", ".join(profile["values"][:2])
    drinking = profile["drinking"]
    smoking = profile["smoking"]
    zodiac_sign = profile["zodiac_sign"]
    mbti_personality_type = profile["mbti_personality_type"]

    # Construct the enriched prompt
    prompt = (
        f"Generate a portrait photo of this human for a dating profile."
        f"{name}, {age}-year-old {gender} ({pronouns}) of {ethnicity} descent and {height} height. "
        f"An {job_industry} professional with an {exercise} physique, valuing {values}. Enjoys {interests}. "
        f"Identifies with {religious_beliefs}, {zodiac_sign}, {mbti_personality_type}. Drinks {drinking}, smokes {smoking}. "
    )

    # Ensure the length is not exceeding 400 characters
    if len(prompt) > 400:
        prompt = prompt[:397] + "..."

    return prompt


def generate_profile_images() -> None:
    # Open and read the user_profiles.jsonl file
    with open('user_profiles.jsonl', 'r') as file:
        for line in file:
            profile = json.loads(line)
            prompt = generate_profile_photo_prompt(profile)
            response = Image.create(
                prompt=prompt,
                response_format="b64_json",
                n=1,
                size="256x256",
            )

            img_data = response["data"][0]["b64_json"]
            image_path = f"./images/{profile['user_id']}.png"
            # save the base 64 image as a png
            with open(image_path, "wb") as fh:
                fh.write(base64.decodebytes(img_data.encode('utf-8')))

            # circuit breaker safety for API cost, comment when ready
            break

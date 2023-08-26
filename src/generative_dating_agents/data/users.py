import json
import os
import random
import uuid
from typing import Collection, Dict, List

from joblib import Parallel, delayed

from ..llm.oai import Conversation, chat_completion
from ..utils.io import write_jsonl_file
from .schemas import user_profile_function_schema
from .types import JsonType


def generate_profiles(
    num_profiles: int,
    model: str,
    output_filename: str,
    max_tokens: int,
    temperature: float,
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

    output_filepath: str = os.path.join(os.getcwd(), f"{output_filename}.jsonl")

    def gen() -> JsonType:
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

        user_profile_json: JsonType = json.loads(user_dating_profile_json_str)

        conversation.add_assistant_message(message=user_dating_profile_json_str)
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

        return user_profile_json

    def parallel_gen() -> List[JsonType]:
        user_profiles_accum: List[JsonType] = Parallel(n_jobs=n_jobs)(
            delayed(gen)() for _ in range(num_profiles)
        )
        return user_profiles_accum

    user_profiles: List[JsonType] = parallel_gen()

    write_jsonl_file(json_array=user_profiles, output_filepath=output_filepath)

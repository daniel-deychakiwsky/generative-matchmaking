import json
import os
import uuid
from typing import Collection, Dict, List

from joblib import Parallel, delayed

from ..llm.oai import Conversation, chat_completion
from ..utils.io import write_jsonl_file
from .schemas import user_profile_function_schema

JsonType = Dict[str, str | bool | int | List[str] | Dict[str, str | bool | int]]


def generate_user_profiles(
    num_profiles: int,
    model: str,
    output_filename: str,
    max_tokens: int,
    temperature: float,
    n_jobs: int = -1,
) -> None:
    output_filepath: str = os.path.join(os.getcwd(), f"{output_filename}.jsonl")
    sys_prompt: str = "You are a helpful assistant."
    gen_prompt: str = "Generate a dating profile. Ensure diversity."
    sum_prompt: str = "Summarize the user's dating profile."
    function_name: str = "set_dating_profile"
    functions: list[dict[str, Collection[str]]] = [
        {"name": function_name, "parameters": user_profile_function_schema}
    ]
    function_call: Dict[str, str] = {"name": function_name}

    def generate() -> JsonType:
        conversation: Conversation = Conversation()
        conversation.add_system_message(message=sys_prompt)
        conversation.add_user_message(message=gen_prompt)
        messages_instruct_generate: List[Dict[str, str]] = conversation.get_messages()
        user_profile_json_str: str = chat_completion(
            model=model,
            messages=messages_instruct_generate,
            max_tokens=max_tokens,
            temperature=temperature,
            functions=functions,
            function_call=function_call,
        )
        user_profile_json: JsonType = json.loads(user_profile_json_str)
        conversation.add_assistant_message(message=user_profile_json_str)
        conversation.add_user_message(message=sum_prompt)
        messages_instruct_summarize: List[Dict[str, str]] = conversation.get_messages()
        user_profile_summary: str = chat_completion(
            model=model,
            messages=messages_instruct_summarize,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        user_profile_json["summary"] = user_profile_summary
        user_profile_json["user_id"] = str(uuid.uuid4())
        return user_profile_json

    def parallel_generate() -> List[JsonType]:
        user_profiles_accum: List[JsonType] = Parallel(n_jobs=n_jobs)(
            delayed(generate)() for _ in range(num_profiles)
        )
        return user_profiles_accum

    user_profiles: List[JsonType] = parallel_generate()

    write_jsonl_file(json_array=user_profiles, output_filepath=output_filepath)


# tune against rate and usage limits
if __name__ == "__main__":
    generate_user_profiles(
        num_profiles=100,
        model="gpt-4-0613",
        output_filename="user_profiles",
        max_tokens=5000,
        temperature=1.05,
        n_jobs=2,
    )

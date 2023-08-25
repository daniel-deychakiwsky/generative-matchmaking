import os
from typing import Dict, List

from ..llm.oai import get_embeddings
from ..utils.io import read_jsonl_file, write_jsonl_file

JsonType = Dict[str, str | List[float]]


def embed_user_profile_summaries(
    model: str,
    input_filename: str,
    output_filename: str,
) -> None:
    input_filepath: str = os.path.join(os.getcwd(), f"{input_filename}.jsonl")
    output_filepath: str = os.path.join(os.getcwd(), f"{output_filename}.jsonl")

    user_profiles: List[Dict[str, str]] = [
        {"user_id": p["user_id"], "summary": p["summary"]}
        for p in read_jsonl_file(input_filepath=input_filepath)
    ]
    user_profile_summaries: List[str] = [p["summary"] for p in user_profiles]
    user_profile_embeddings: List[List[float]] = get_embeddings(
        model=model, text=user_profile_summaries
    )
    user_profile_id_embeddings: List[JsonType] = [
        {"user_id": p["user_id"], "embedding": e}
        for p, e in zip(user_profiles, user_profile_embeddings)
    ]

    write_jsonl_file(
        json_array=user_profile_id_embeddings, output_filepath=output_filepath
    )


if __name__ == "__main__":
    embed_user_profile_summaries(
        model="text-embedding-ada-002",
        input_filename="user_profiles",
        output_filename="user_profiles_embedding",
    )

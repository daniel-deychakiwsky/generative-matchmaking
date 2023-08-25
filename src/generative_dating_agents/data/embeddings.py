import os
from typing import Dict, List

import jsonlines

from ..llm.oai import get_embeddings

JsonType = Dict[str, str | List[float]]


def embed_user_profile_summaries(
    model: str,
    input_filename: str,
    output_filename: str,
) -> None:
    input_filepath: str = os.path.join(os.getcwd(), f"{input_filename}.jsonl")
    output_filepath: str = os.path.join(os.getcwd(), f"{output_filename}.jsonl")

    with jsonlines.open(input_filepath, "r") as user_profile_reader:
        user_profiles: List[Dict[str, str]] = [
            {"user_id": p["user_id"], "summary": p["summary"]}
            for p in user_profile_reader
        ]
        user_profile_summaries: List[str] = [p["summary"] for p in user_profiles]
        user_profile_embeddings: List[List[float]] = get_embeddings(
            model=model, text=user_profile_summaries
        )
        user_profile_id_embeddings: List[JsonType] = [
            {"user_id": p["user_id"], "embedding": e}
            for p, e in zip(user_profiles, user_profile_embeddings)
        ]

    with jsonlines.open(output_filepath, "w") as writer:
        writer.write_all(user_profile_id_embeddings)


if __name__ == "__main__":
    embed_user_profile_summaries(
        model="text-embedding-ada-002",
        input_filename="user_profiles",
        output_filename="user_profiles_embedding",
    )

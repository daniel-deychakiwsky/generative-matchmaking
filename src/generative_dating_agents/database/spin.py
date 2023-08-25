import os

from ..utils.io import read_jsonl_file
from .chroma import ChromaVectorDatabase


def initialize(input_filename: str) -> None:
    input_filepath: str = os.path.join(os.getcwd(), f"{input_filename}.jsonl")
    user_profiles = read_jsonl_file(input_filepath=input_filepath)
    user_ids = [p["user_id"] for p in user_profiles]
    user_profile_summaries = [p["summary"] for p in user_profiles]

    collection_name = "user_profiles"
    vdb = ChromaVectorDatabase()
    vdb.create_collection(name=collection_name)
    vdb.add_to_collection(
        name=collection_name,
        ids=user_ids,
        documents=user_profile_summaries,
    )

    query_result = vdb.query_collection(
        name=collection_name,
        query_texts=["I want a woman that that plays soccer or tennis"],
        n_results=1,
        where=None,
        where_document=None,
    )

    print(query_result)


if __name__ == "__main__":
    initialize(input_filename="user_profiles")

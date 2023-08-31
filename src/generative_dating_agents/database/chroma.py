import os
from typing import List, Optional

import chromadb
from chromadb.api.models.Collection import (
    ID,
    Document,
    EmbeddingFunction,
    Metadata,
    OneOrMany,
    QueryResult,
    Where,
    WhereDocument,
)
from chromadb.config import Settings
from chromadb.utils import embedding_functions

from ..data.schemas import UserProfile
from ..utils.io import read_user_profile_from_json

DEFAULT_USER_PROFILES_COLLECTION_NAME: str = "user_profiles"
DEFAULT_DISTANCE: str = "cos"


class ChromaVectorDatabaseClient:
    def __init__(self) -> None:
        self.client = chromadb.HttpClient(
            host="localhost", port="8000", settings=Settings(anonymized_telemetry=False)
        )

    def create_collection(self, name: str, distance: str = DEFAULT_DISTANCE) -> None:
        embedding_function: Optional[
            EmbeddingFunction
        ] = embedding_functions.DefaultEmbeddingFunction()
        self.client.create_collection(
            name,
            get_or_create=True,
            embedding_function=embedding_function,
            metadata={"hnsw:space": distance},
        )

    def add_to_collection(
        self,
        name: str,
        ids: OneOrMany[ID],
        documents: Optional[OneOrMany[Document]],
        meta_datas: Optional[OneOrMany[Metadata]] = None,
    ) -> None:
        self.client.get_collection(name=name).add(
            ids=ids,
            documents=documents,
            metadatas=meta_datas,
        )

    def query_collection(
        self,
        name: str,
        query_texts: Optional[OneOrMany[Document]],
        n_results: int = 2,
        where: Optional[Where] = None,
        where_document: Optional[WhereDocument] = None,
    ) -> QueryResult:
        query_result: QueryResult = self.client.get_collection(name=name).query(
            query_texts=query_texts,
            n_results=n_results,
            where=where,
            where_document=where_document,
        )

        return query_result

    def delete_collection(
        self,
        name: str,
    ) -> None:
        self.client.delete_collection(name=name)

    def count_collection(self, collection_name: str) -> int:
        return self.client.get_collection(name=collection_name).count()


def load_user_profile_collection(
    input_directory: str,
    input_file_name: str,
    collection_name: str = DEFAULT_USER_PROFILES_COLLECTION_NAME,
    distance: str = DEFAULT_DISTANCE,
    verbose: bool = False,
) -> None:
    input_directory_path: str = os.path.join(os.getcwd(), input_directory)
    user_profiles: List[UserProfile] = [
        read_user_profile_from_json(
            file_path=os.path.join(input_directory_path, d, input_file_name)
        )
        for d in os.listdir(input_directory_path)
        if os.path.isdir(os.path.join(input_directory_path, d))
    ]

    user_ids: List[str] = [p.user_id for p in user_profiles]
    user_profile_summaries: List[str] = [p.profile_summary for p in user_profiles]
    user_profile_preferences_summaries: Optional[OneOrMany[Metadata]] = [
        {"preferences_summary": p.preferences_summary} for p in user_profiles
    ]

    vdb: ChromaVectorDatabaseClient = ChromaVectorDatabaseClient()
    vdb.create_collection(name=collection_name, distance=distance)
    vdb.add_to_collection(
        name=collection_name,
        ids=user_ids,
        documents=user_profile_summaries,
        meta_datas=user_profile_preferences_summaries,
    )

    if verbose:
        print(
            "Collection item count:",
            vdb.count_collection(collection_name=collection_name),
        )


def query_user_profile_collection(
    query_texts: Optional[OneOrMany[Document]],
    n_results: int,
    collection_name: str = DEFAULT_USER_PROFILES_COLLECTION_NAME,
    where: Optional[Where] = None,
    where_document: Optional[WhereDocument] = None,
    verbose: bool = False,
) -> QueryResult:
    vdb: ChromaVectorDatabaseClient = ChromaVectorDatabaseClient()

    query_result: QueryResult = vdb.query_collection(
        name=collection_name,
        query_texts=query_texts,
        n_results=n_results,
        where=where,
        where_document=where_document,
    )

    if verbose:
        print(query_result)

    return query_result


def delete_user_profile_collection(
    collection_name: str = DEFAULT_USER_PROFILES_COLLECTION_NAME,
) -> None:
    vdb: ChromaVectorDatabaseClient = ChromaVectorDatabaseClient()
    vdb.delete_collection(name=collection_name)

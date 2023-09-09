from typing import List, Optional

from chromadb.api.models.Collection import (
    Document,
    Metadata,
    OneOrMany,
    QueryResult,
    Where,
    WhereDocument,
)

from ..data.user_profile import UserProfile
from ..utils.constants import (
    CHROMA_DISTANCE,
    CHROMA_PERSISTENT_PATH,
    CHROMA_USER_PROFILES_COLLECTION_NAME,
)
from ..utils.io import read_all_user_profiles
from .chroma import ChromaVectorDatabaseClient

vdb: ChromaVectorDatabaseClient = ChromaVectorDatabaseClient(
    path=CHROMA_PERSISTENT_PATH
)


def load_user_profile_collection(
    collection_name: str = CHROMA_USER_PROFILES_COLLECTION_NAME,
    distance: str = CHROMA_DISTANCE,
    verbose: bool = False,
) -> None:
    user_profiles: List[UserProfile] = read_all_user_profiles()
    user_ids: List[str] = [p.user_id for p in user_profiles]
    user_profile_summaries: List[str] = [p.profile_summary for p in user_profiles]
    user_profile_metadata: Optional[OneOrMany[Metadata]] = [
        {"gender": p.gender, "sexuality": p.sexuality} for p in user_profiles
    ]
    vdb.create_collection(name=collection_name, distance=distance)
    vdb.add_to_collection(
        name=collection_name,
        ids=user_ids,
        documents=user_profile_summaries,
        metadatas=user_profile_metadata,
    )

    if verbose:
        print(
            "Collection count:",
            vdb.count_collection(name=collection_name),
        )


def query_user_profile_collection(
    query_texts: Optional[OneOrMany[Document]],
    n_results: int,
    collection_name: str = CHROMA_USER_PROFILES_COLLECTION_NAME,
    where: Optional[Where] = None,
    where_document: Optional[WhereDocument] = None,
    verbose: bool = False,
) -> QueryResult:
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
    collection_name: str = CHROMA_USER_PROFILES_COLLECTION_NAME,
) -> None:
    vdb.delete_collection(name=collection_name)

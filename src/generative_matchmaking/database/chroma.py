from typing import Optional

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

from ..utils.constants import CHROMA_DISTANCE_KEY


class ChromaVectorDatabaseClient:
    def __init__(self, path: str) -> None:
        self.client = chromadb.PersistentClient(
            path=path,
            settings=Settings(anonymized_telemetry=False),
        )

    def create_collection(self, name: str, distance: str) -> None:
        embedding_function: Optional[
            EmbeddingFunction
        ] = embedding_functions.DefaultEmbeddingFunction()
        self.client.create_collection(
            name,
            get_or_create=True,
            embedding_function=embedding_function,
            metadata={CHROMA_DISTANCE_KEY: distance},
        )

    def add_to_collection(
        self,
        name: str,
        ids: OneOrMany[ID],
        documents: Optional[OneOrMany[Document]],
        metadatas: Optional[OneOrMany[Metadata]] = None,
    ) -> None:
        self.client.get_collection(name=name).add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
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

    def count_collection(self, name: str) -> int:
        return self.client.get_collection(name=name).count()

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
from chromadb.utils import embedding_functions


class ChromaVectorDatabase:
    def __init__(self) -> None:
        self.client = chromadb.Client()

    def create_collection(self, name: str) -> None:
        embedding_function: Optional[
            EmbeddingFunction
        ] = embedding_functions.DefaultEmbeddingFunction()
        self.client.create_collection(
            name, get_or_create=True, embedding_function=embedding_function
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
        return self.client.get_collection(name=name).query(
            query_texts=query_texts,
            n_results=n_results,
            where=where,
            where_document=where_document,
        )

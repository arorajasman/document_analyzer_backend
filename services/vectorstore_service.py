import os
from typing import List

from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_core.documents import Document


class VectorStoreService:
    """Service to connect with the database"""

    # instance to get access to vector store
    vector_store: PGVector

    def __init__(self) -> None:
        self.embeddings = OpenAIEmbeddings(
            # model="text-embedding-3-large",
            api_key=os.getenv("OPEN_API_KEY"),
            timeout=10000,
            max_retries=5,
        )
        self.collection_name = "document_analyzer_docs"
        self.connection = os.getenv("PG_VECTOR_DATABASE_URL")
        self.create_vector_store()

    def get_vector_store(self):
        return self.vector_store

    def create_vector_store(self):
        """Method to create a vector store"""

        self.vector_store = PGVector(
            embeddings=self.embeddings,
            collection_name=self.collection_name,
            connection=self.connection,
            use_jsonb=True,
        )

    def store_documents_in_db(self, documents: List[Document]):
        """
        Method to store the splitted document chunks in the vector database
        """

        try:
            BATCH_SIZE = 10
            for index in range(0, len(documents), BATCH_SIZE):
                docs_batch = documents[index: index + 10]  # noqa: E203
                self.vector_store.add_documents(docs_batch)
        except Exception as e:
            raise e

    def get_document_with_similarity(self, key: str):
        """
        Method to get the document from the vector database based on similarity
        """
        try:
            document: List[Document] = self.vector_store.similarity_search(
                key, k=20
            )  # noqa
            return document
        except Exception as e:
            raise e

    def get_retriver(self):
        return self.vector_store.as_retriver()

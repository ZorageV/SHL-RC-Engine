import time
from typing import List, Dict, Any
from pinecone import Pinecone, ServerlessSpec
from app.config import PINECONE_API_KEY, PINECONE_INDEX_NAME


class PineconeDatabase:
    """A class to handle Pinecone database operations."""

    def __init__(self, api_key: str = None, index_name: str = None):
        """Initialize the database connection."""
        self.pc = Pinecone(api_key=api_key or PINECONE_API_KEY)
        self.index_name = index_name or PINECONE_INDEX_NAME
        self.namespace = "shl-tests"
        self.index = self._initialize_index()

    def _initialize_index(self) -> Any:
        """Initialize or create the Pinecone index."""
        try:
            return self.pc.Index(self.index_name)
        except Exception:
            self.pc.create_index(
                name=self.index_name,
                dimension=1024,  # Dimension for multilingual-e5-large model
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
            # Wait for the index to be ready
            while not self.pc.describe_index(self.index_name).status["ready"]:
                time.sleep(1)
            return self.pc.Index(self.index_name)

    def add_tests(self, data: List[Any], input_type: str = "passage") -> List[Dict]:
        """Upsert vectors to the database."""
        # Extract descriptions from test objects
        # print(data)
        for i in range(0, len(data)):
            batch_data = data[i : i + 50]
            descriptions = [test["description"] for test in batch_data]
            embedding_response = self.pc.inference.embed(
                model="multilingual-e5-large",
                inputs=descriptions,
                parameters={"input_type": input_type, "truncate": "END"},
            )

            # Extract the actual vector values from the embedding response
            embeddings = [embedding["values"] for embedding in embedding_response]

            # Prepare vectors for upserting
            vectors = []
            for test, embedding in zip(batch_data, embeddings):
                vectors.append(
                    {
                        "id": f"{test['id']}",
                        "values": embedding,
                        "metadata": {
                            "id": test["id"],
                            "name": test["name"],
                            "link": test["link"],
                            "remote_testing": test["remote_testing"],
                            "adaptive_irt": test["adaptive_irt"],
                            "test_type": test["test_type"],
                            "description": test["description"],
                            "full_link": test["full_link"],
                            "job_levels": test["job_levels"],
                            "languages": test["languages"],
                            "assessment_length": test["assessment_length"],
                        },
                    }
                )

            # Upsert vectors to the database
            self.index.upsert(vectors=vectors, namespace=self.namespace)
        return True

    def query(self, query: List[float], top_k: int) -> List[Dict]:
        """Query vectors from the database."""
        if top_k==0:
            top_k = 1
        top_k = min(10, top_k)
        embedding = self.pc.inference.embed(
            model="multilingual-e5-large",
            inputs=[query],
            parameters={"input_type": "query"},
        )

        results = self.index.query(
            namespace=self.namespace,
            vector=embedding[0]["values"],
            top_k=top_k,
            include_values=False,
            include_metadata=True,
        )
        return results.matches

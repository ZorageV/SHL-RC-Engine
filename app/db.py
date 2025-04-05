import time
from pinecone import Pinecone, ServerlessSpec

# Initialize Pinecone client
pc = Pinecone(
    api_key="pcsk_2ETskL_7RRsmCihFTJphq7hZ8UMcxrqJR72idNbJQV4f2EenqkpMBAVZSqgDY4oajCCLqj"
)
index_name = "prod"

# Create or get the index
try:
    index = pc.Index(index_name)
except Exception:
    pc.create_index(
        name=index_name,
        dimension=1024,  # Dimension for multilingual-e5-large model
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    # Wait for the index to be ready
    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)
    index = pc.Index(index_name)

import json

# Load the data from data.json
with open("processed_data.json", "r", encoding="utf-8") as file:
    datat = json.load(file)

# Generate embeddings for the descriptions
for i in range(0,len(datat)):
    data = datat[i:i+50]
    embeddings = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[d["description"] for d in data],
        parameters={"input_type": "passage", "truncate": "END"},
    )

    # Prepare vectors for upserting to Pinecone
    vectors = []
    for d, e in zip(data, embeddings):
        vectors.append(
            {
                "id": d["id"],
                "values": e["values"],
                "metadata": {
                    "id": d["id"],
                    "description": d["description"],
                },
            }
        )

    # Upsert vectors to Pinecone
    index.upsert(vectors=vectors, namespace="dev")
# print(index.describe_index_stats())

# Example query
query = "Looking to hire mid-level professionals who are proficient in Python, SQL and Java Script. Need an assessment package that can test all skills with max duration of 60 minutes."

# Generate embedding for the query
embedding = pc.inference.embed(
    model="multilingual-e5-large", inputs=[query], parameters={"input_type": "query"}
)

# Search for similar assessments
results = index.query(
    namespace="dev",
    vector=embedding[0]["values"],
    top_k=3,
    include_values=False,
    include_metadata=True,
)

print(results)

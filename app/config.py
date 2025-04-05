import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Pinecone configuration
PINECONE_API_KEY = os.getenv(
    "PINECONE_API_KEY",
    "pcsk_2ETskL_7RRsmCihFTJphq7hZ8UMcxrqJR72idNbJQV4f2EenqkpMBAVZSqgDY4oajCCLqj",
)
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "prod")

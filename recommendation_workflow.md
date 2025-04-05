# Recommendation Workflow

### Step 1: Extract Data
- Data is extracted from the SHL assessment product page.

### Step 2: Clean Data
- The extracted data is cleaned and formatted into a relevant structure.

### Data Format for Each Assessment

The data extracted for each assessment is structured as follows:

```python
name = Column(String, index=True)
link = Column(String)
remote_testing = Column(String)
adaptive_irt = Column(String)
test_type = Column(ARRAY(String))
description = Column(Text)
full_link = Column(String)
job_levels = Column(ARRAY(String))
languages = Column(ARRAY(String))
assessment_length = Column(Integer)
```

### Step 3: Store Data in PostgreSQL
- The cleaned data is stored in a PostgreSQL database for structured storage and retrieval.

### Step 4: Generate and Store Embeddings in Pinecone
- Embeddings are generated based on the `description` field of each assessment using a machine learning model.
- The model used is `multilingual-e5-large` with the following parameters:
- The embeddings are then stored in the Pinecone vector database.

### Step 5: Query Pinecone
- Pinecone's inbuilt query engine is used to retrieve outputs and top-k results based on similarity.

### Step 6: Filter Results
- Outputs are filtered based on the given time and cosine similarity score (above 0.5).
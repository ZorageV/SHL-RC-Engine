# AI Recommendation Engine

A modern assessment recommendation system based on job search that helps HRs create anf find different tests for job descriptions (JDs).

## Tech Stack
- **Backend**: FastAPI, Python 3.11
- **Database**: PostgreSQL (via SQLAlchemy)
- **Vector Database**: Pinecone
- **Frontend**: React (hosted on Vercel)
- **Containerization**: Docker
- **Deployment**: AWS EC2

## Databases Used
1. **PostgreSQL**: For structured data storage.
2. **Pinecone**: For semantic search and vector similarity queries.

## Main Workflow Diagram
```plaintext
+-------------------+        +-------------------+        +-------------------+ 
|   Frontend (UI)   | -----> |   FastAPI Backend | -----> |   PostgreSQL DB   |
+-------------------+        +-------------------+        +-------------------+
         |                          |                           |
         v                          v                           v
+-------------------+        +-------------------+        +-------------------+
|  User Requests    |        |  Pinecone Vector  |        |  Data Retrieval   |
|  (Search/Tests)   | -----> |  Similarity Query | -----> |  & Storage        |
+-------------------+        +-------------------+        +-------------------+
```

## Repository

The source code for this project is available on GitHub:  
- [Backend Code](https://github.com/ZorageV/SHL-RC-Engine/tree/main/BE)  
- [Frontend Code](https://github.com/ZorageV/SHL-RC-Engine-FE)

## Deployment

The application is deployed using the following tools:
- **Nginx**: Used as a reverse proxy to route traffic to the backend and frontend.
- **Certbot SSL**: Configured for HTTPS using Let's Encrypt certificates.
- **Docker**: Containerized deployment for consistent environments.

- **Backend**: Deployed on AWS EC2.
- **Frontend**: Hosted on Vercel.

## Key Features
- User authentication with JWT.
- Bulk test creation and semantic search using Pinecone.
- Health check and monitoring endpoints.

## API Documentation

### Test Creation API
- **Endpoint**: `/tests/`
- **Method**: `POST`
- **Description**: Allows bulk creation of tests and stores them in the database and Pinecone vector database.
- **Request Body**:
  ```json
  [
    {
      "name": "Test Name",
      "link": "Test Link",
      "remote_testing": "Yes",
      "adaptive_irt": "No",
      "test_type": ["Type1", "Type2"],
      "description": "Test Description",
      "full_link": "Full Test Link",
      "job_levels": ["Level1", "Level2"],
      "languages": ["Language1", "Language2"],
      "assessment_length": "30"
    }
  ]
  ```
- **Response**:
  ```json
  {
    "test_ids": [1, 2, 3]
  }
  ```

### Search API
- **Endpoint**: `/search/`
- **Method**: `POST`
- **Description**: Performs semantic search for tests using Pinecone and retrieves matching test details.
- **Request Body**:
  ```json
  {
    "query": "Search query",
    "top_k": 5,
    "time": 30
  }
  ```
- **Response**:
  ```json
  {
    "matches": [
      {
        "id": "1",
        "score": 0.95,
        "metadata": {
          "name": "Test Name",
          "description": "Test Description",
          "link": "Test Link",
          "remote_testing": "Yes",
          "adaptive_irt": "No",
          "test_type": ["Type1", "Type2"],
          "full_link": "Full Test Link",
          "job_levels": ["Level1", "Level2"],
          "languages": ["Language1", "Language2"],
          "assessment_length": "30"
        }
      }
    ]
  }
  ```

## Recommendation Workflow

For detailed information about the recommendation workflow, refer to the [Recommendation Workflow Documentation](./recommendation_workflow.md).
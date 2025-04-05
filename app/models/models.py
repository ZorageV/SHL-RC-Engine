from typing import Optional, List
from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None


class TestBase(BaseModel):
    name: str
    link: Optional[str] = None
    remote_testing: Optional[str] = None
    adaptive_irt: Optional[str] = None
    test_type: Optional[List[str]] = None
    description: Optional[str] = None
    full_link: Optional[str] = None
    job_levels: Optional[List[str]] = None
    languages: Optional[List[str]] = None
    assessment_length: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Administrative Professional - Short Form",
                "link": "/solutions/products/product-catalog/view/administrative-professional-short-form/",
                "remote_testing": "Yes",
                "adaptive_irt": "Yes",
                "test_type": [
                    "Ability & Aptitude",
                    "Knowledge & Skills",
                    "Personality & Behavior",
                ],
                "full_link": "https://www.shl.com/solutions/products/product-catalog/view/administrative-professional-short-form/",
                "description": "The Administrative Professional solution is for entry to mid-level positions...",
                "job_levels": ["Entry-Level"],
                "languages": ["English (USA)"],
                "assessment_length": "36",
            }
        }


class TestCreate(TestBase):
    pass


class TestResponse(TestBase):
    id: int

    class Config:
        from_attributes = True


class TestResponseList(BaseModel):
    tests: List[TestResponse]

    class Config:
        from_attributes = True


class ConflictStrategy(str, Enum):
    SKIP = "skip"  # Skip tests that already exist
    UPDATE = "update"  # Update existing tests
    FAIL = "fail"  # Fail if any test already exists


class BulkTestCreate(BaseModel):
    tests: List[TestCreate]
    conflict_strategy: ConflictStrategy = ConflictStrategy.FAIL


class PineconeQueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 1
    time: Optional[int] = 30


class PineconeMatch(BaseModel):
    id: str
    score: float
    metadata: dict


class PineconeQueryResponse(BaseModel):
    matches: List[PineconeMatch]


class SearchEvaluationMetrics(BaseModel):
    mean_recall_at_k: float
    mean_average_precision_at_k: float
    k: int
    total_queries: int


class SearchEvaluationRequest(BaseModel):
    queries: List[str]
    relevant_test_ids: List[
        List[int]
    ]  # List of lists, where each inner list contains relevant test IDs for each query
    k: int = 3  # Default to 3, matching our current top_k

from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.models import (
    Token,
    User,
    UserCreate,
    TestCreate,
    TestResponseList,
    PineconeQueryRequest,
    PineconeQueryResponse,
    PineconeMatch,
)
from app.auth import (
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_password_hash,
)
from app.database import get_db, User as DBUser, Test as DBTest
from app.services.pinecone_db import PineconeDatabase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Recommendation Engine")

# Initialize Pinecone database
pinecone_db = PineconeDatabase()

# Configure CORS
origins = os.environ.get("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Update the `get_db` dependency to use the updated engine
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Welcome to the AI Recommendation Engine API"}


@app.get("/health")
async def health_check():
    """
    Health check endpoint to monitor server status.
    Returns a 200 OK status with server information.
    """
    return {
        "status": "healthy",
        "service": "AI Recommendation Engine",
        "version": "1.0.0",
    }


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Login endpoint that authenticates users and returns a JWT token.
    """
    logger.info(f"Login attempt for user: {form_data.username}")
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning(f"Invalid login attempt for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=int(
            os.environ.get(
                "ACCESS_TOKEN_EXPIRE_MINUTES", str(ACCESS_TOKEN_EXPIRE_MINUTES)
            )
        )
    )
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/{id}", response_model=User)
async def read_users_me(id: int, db: Session = Depends(get_db)):
    """
    Endpoint that returns user information by ID.
    """
    user = db.query(DBUser).filter(DBUser.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    # Check if username already exists
    db_user = db.query(DBUser).filter(DBUser.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # Check if email already exists (if provided)
    if user.email:
        db_user = db.query(DBUser).filter(DBUser.email == user.email).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = DBUser(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        disabled=False,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.post("/tests/", status_code=status.HTTP_201_CREATED)
async def create_tests(
    tests: List[TestCreate],
    db: Session = Depends(get_db),
):
    """
    Create multiple tests in bulk and return their IDs as an array.
    """
    db_tests = [
        DBTest(
            name=test.name,
            link=test.link,
            remote_testing=test.remote_testing,
            adaptive_irt=test.adaptive_irt,
            test_type=test.test_type,
            description=test.description,
            full_link=test.full_link,
            job_levels=test.job_levels,
            languages=test.languages,
            assessment_length=test.assessment_length,
        )
        for test in tests
    ]

    db.bulk_save_objects(db_tests)
    db.commit()

    test_names = [test.name for test in tests]
    inserted_tests = db.query(DBTest).filter(DBTest.name.in_(test_names)).all()
    test_ids = [test.id for test in inserted_tests]

    pinecone_data = []
    for test, db_test in zip(tests, inserted_tests):
        pinecone_data.append(
            {
                "id": str(db_test.id),
                "name": test.name,
                "description": test.description,
                "link": test.link,
                "remote_testing": test.remote_testing,
                "adaptive_irt": test.adaptive_irt,
                "test_type": test.test_type,
                "full_link": test.full_link,
                "job_levels": test.job_levels,
                "languages": test.languages,
                "assessment_length": test.assessment_length,
            }
        )

    if pinecone_data:
        pinecone_db.add_tests(pinecone_data)

    return {"test_ids": test_ids}


@app.post("/search/", response_model=PineconeQueryResponse)
async def search_tests(
    query_request: PineconeQueryRequest,
    db: Session = Depends(get_db),
):
    """
    Search for tests using semantic similarity.
    """
    matches = pinecone_db.query(query_request.query, top_k=query_request.top_k)

    test_ids = [int(match.id) for match in matches]
    tests = db.query(DBTest).filter(DBTest.id.in_(test_ids)).all()

    test_dict = {test.id: test for test in tests}

    pinecone_matches = []
    for match in matches:
        test_id = int(match.id)
        match_obj = PineconeMatch(
            id=match.id, score=match.score, metadata=match.metadata
        )

        if test_id in test_dict:
            test_data = test_dict[test_id]
            match_obj.metadata.update(
                {
                    "name": test_data.name,
                    "description": test_data.description,
                    "link": test_data.link,
                    "remote_testing": test_data.remote_testing,
                    "adaptive_irt": test_data.adaptive_irt,
                    "test_type": test_data.test_type,
                    "full_link": test_data.full_link,
                    "job_levels": test_data.job_levels,
                    "languages": test_data.languages,
                    "assessment_length": test_data.assessment_length,
                }
            )

            if test_data.assessment_length:
                try:
                    assessment_length = int(test_data.assessment_length)
                    if assessment_length > query_request.time:
                        continue
                except (ValueError, TypeError):
                    pass

        pinecone_matches.append(match_obj)

    return PineconeQueryResponse(matches=pinecone_matches)

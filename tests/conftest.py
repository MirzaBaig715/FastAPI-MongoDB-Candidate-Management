import pytest

from motor.motor_asyncio import AsyncIOMotorClient

from src.config.settings import get_settings
from src.domain.repositories.candidate_repository import CandidateRepository
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.database import Database
from src.services.auth_service import AuthService
from src.services.candidate_service import CandidateService

settings = get_settings()


@pytest.fixture
async def db():
    """Database fixture."""
    test_db = Database()
    test_db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    test_db.db = test_db.client[f'{settings.MONGODB_DB_NAME}_test']

    yield test_db

    await test_db.client.drop_database(test_db.db)
    test_db.client.close()


@pytest.fixture
def user_repository(db):
    """User repository fixture."""
    return UserRepository(db.db.users)


@pytest.fixture
def candidate_repository(db):
    """Candidate repository fixture."""
    return CandidateRepository(db.db.candidates)


@pytest.fixture
def auth_service(user_repository):
    """Auth service fixture."""
    return AuthService(user_repository)


@pytest.fixture
def candidate_service(candidate_repository):
    """Candidate service fixture."""
    return CandidateService(candidate_repository)

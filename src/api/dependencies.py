from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.core.security import verify_token
from src.domain.repositories.user_repository import UserRepository
from src.domain.repositories.candidate_repository import CandidateRepository
from src.infrastructure.database import db
from src.services.auth_service import AuthService
from src.services.candidate_service import CandidateService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_token(token)
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception

    user_repo = UserRepository(db.db.users)
    user = await user_repo.get_by_email(email)
    if user is None:
        raise credentials_exception
    return user


def get_auth_service():
    """Get auth service instance."""
    return AuthService(UserRepository(db.db.users))


def get_candidate_service():
    """Get candidate service instance."""
    return CandidateService(CandidateRepository(db.db.candidates))

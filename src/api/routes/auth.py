from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.api.dependencies import get_auth_service
from src.domain.models.user import User, UserCreate
from src.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=User)
async def register(
    user: UserCreate, auth_service: AuthService = Depends(get_auth_service)
):
    """Register a new user."""
    try:
        return await auth_service.create_user(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
):
    """Login to get access token."""
    user = await auth_service.authenticate_user(
        form_data.username,
        form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return auth_service.create_token(user)

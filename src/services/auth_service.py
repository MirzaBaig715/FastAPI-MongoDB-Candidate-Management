from typing import Optional
from src.core.security import verify_password, create_access_token, get_password_hash
from src.domain.models.user import UserCreate, User, UserInDB
from src.domain.repositories.user_repository import UserRepository


class AuthService:
    """Authentication service."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def authenticate_user(
            self,
            email: str,
            password: str
    ) -> Optional[UserInDB]:
        """Authenticate a user."""
        user = await self.user_repository.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    async def create_user(self, user_create: UserCreate) -> User:
        """Create a new user."""
        existing_user = await self.user_repository.get_by_email(user_create.email)
        if existing_user:
            raise ValueError("Email already registered")

        hashed_password = get_password_hash(user_create.password)
        user_data = user_create.model_dump()
        user_data["password"] = hashed_password

        user_db = await self.user_repository.create(UserCreate(**user_data))
        return User(**user_db.model_dump(exclude={"hashed_password"}))

    @staticmethod
    def create_token(user: UserInDB) -> dict:
        """Create access token for user."""
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}

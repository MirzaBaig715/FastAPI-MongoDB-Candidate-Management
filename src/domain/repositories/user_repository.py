from typing import Optional
from bson import ObjectId
from src.domain.models.user import UserInDB, UserCreate
from .base import BaseRepository


class UserRepository(BaseRepository[UserInDB]):
    """User repository implementation."""

    async def create(self, user: UserCreate) -> UserInDB:
        user_dict = user.model_dump()
        user_db = UserInDB(**user_dict, hashed_password=user.password)
        result = await self.collection.insert_one(user_db.model_dump())
        user_db.id = str(result.inserted_id)
        return user_db

    async def get(self, id: str) -> Optional[UserInDB]:
        if user_dict := await self.collection.find_one({"_id": ObjectId(id)}):
            return UserInDB(**user_dict)
        return None

    async def get_by_email(self, email: str) -> Optional[UserInDB]:
        if user_dict := await self.collection.find_one({"email": email}):
            return UserInDB(**user_dict)
        return None

    async def update(self, id: str, user: UserInDB) -> Optional[UserInDB]:
        update_data = user.model_dump(exclude={"id"})
        result = await self.collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
        if result.modified_count:
            return await self.get(id)
        return None

    async def delete(self, id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return bool(result.deleted_count)
from datetime import datetime
from typing import Optional, List
from bson import ObjectId
from src.domain.models.candidate import CandidateInDB, CandidateCreate, CandidateUpdate
from .base import BaseRepository


class CandidateRepository(BaseRepository[CandidateInDB]):
    """Candidate repository implementation."""

    async def create(self, candidate: CandidateCreate) -> CandidateInDB:
        candidate_dict = candidate.model_dump()
        candidate_db = CandidateInDB(**candidate_dict)
        result = await self.collection.insert_one(candidate_db.model_dump())
        candidate_db.id = str(result.inserted_id)
        return candidate_db

    async def get(self, id: str) -> Optional[CandidateInDB]:
        if candidate_dict := await self.collection.find_one({"_id": ObjectId(id)}):
            return CandidateInDB(**candidate_dict)
        return None

    async def get_by_email(self, email: str) -> Optional[CandidateInDB]:
        if candidate_dict := await self.collection.find_one({"email": email}):
            return CandidateInDB(**candidate_dict)
        return None

    async def update(self, id: str, candidate: CandidateUpdate) -> Optional[CandidateInDB]:
        update_data = {
            k: v for k, v in candidate.model_dump(exclude_unset=True).items()
            if v is not None
        }
        if not update_data:
            return await self.get(id)

        update_data["updated_at"] = datetime.utcnow()
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

    async def search(
            self,
            query: str,
            skip: int = 0,
            limit: int = 10
    ) -> tuple[List[CandidateInDB], int]:
        """Search candidates with pagination."""
        filter_query = {
            "$or": [
                {"full_name": {"$regex": query, "$options": "i"}},
                {"position": {"$regex": query, "$options": "i"}},
                {"skills": {"$in": [query]}},
            ]
        }

        total = await self.collection.count_documents(filter_query)
        cursor = self.collection.find(filter_query).skip(skip).limit(limit)

        candidates = []
        async for doc in cursor:
            candidates.append(CandidateInDB(**doc))

        return candidates, total

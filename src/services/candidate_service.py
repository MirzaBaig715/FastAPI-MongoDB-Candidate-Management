import csv
from io import StringIO
from typing import List, Optional, Tuple

from src.core.exceptions import DataValidationError, NotFoundError
from src.domain.models.candidate import (
    Candidate,
    CandidateCreate,
    CandidateUpdate
)
from src.domain.repositories.candidate_repository import CandidateRepository


class CandidateService:
    """Candidate service implementation."""

    def __init__(self, candidate_repository: CandidateRepository):
        self.candidate_repository = candidate_repository

    async def create_candidate(
            self, candidate: CandidateCreate
    ) -> Optional[Candidate]:
        """Create a new candidate."""
        candidate.email = candidate.email.strip()
        if await self.candidate_repository.get_by_email(candidate.email):
            raise DataValidationError(
                "Candidate with this email already exists."
            )
        candidate_db = await self.candidate_repository.create(candidate)
        return Candidate(**candidate_db.model_dump())

    async def get_candidate(self, id: str) -> Candidate:
        """Get a candidate by ID."""
        if candidate := await self.candidate_repository.get(id):
            return Candidate(**candidate.model_dump())
        raise NotFoundError(f"Candidate with ID {id} not found")

    async def update_candidate(
        self, id: str, candidate: CandidateUpdate
    ) -> Optional[Candidate]:
        """Update a candidate."""
        statuses = (
            "applied",
            "screening",
            "interviewed",
            "offered",
            "hired",
            "rejected",
        )
        if candidate.status and candidate.status not in statuses:
            raise DataValidationError(
                f"status should be one of them: {statuses}"
            )
        if updated := await self.candidate_repository.update(id, candidate):
            return Candidate(**updated.model_dump())
        raise NotFoundError(f"Candidate with ID {id} not found")

    async def delete_candidate(self, id: str) -> bool:
        """Delete a candidate."""
        if not await self.candidate_repository.delete(id):
            raise NotFoundError(f"Candidate with ID {id} not found")
        return True

    async def search_candidates(
        self, query: str = "", skip: int = 0, limit: int = 10
    ) -> Tuple[List[Candidate], int]:
        """Search candidates with pagination."""
        candidates, total = await self.candidate_repository.search(
            query=query, skip=skip, limit=limit
        )
        return [Candidate(**c.model_dump()) for c in candidates], total

    async def generate_report(self, skip: int = 0, limit: int = 100) -> str:
        """Generate CSV report of all candidates with pagination."""
        output = StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=[
                "id",
                "full_name",
                "email",
                "position",
                "experience",
                "skills",
                "status",
                "created_at",
                "updated_at",
            ],
        )
        writer.writeheader()

        cursor = (
            self.candidate_repository.collection.find().skip(skip).limit(limit)
        )  # noqa: E501
        async for candidate in cursor:
            candidate["id"] = str(candidate["_id"])
            candidate["skills"] = ", ".join(candidate["skills"])
            candidate.pop("_id", None)
            writer.writerow(candidate)

        return output.getvalue()

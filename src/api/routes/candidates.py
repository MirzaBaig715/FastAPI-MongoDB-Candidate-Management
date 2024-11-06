from fastapi import APIRouter, Depends, Query, Response

from src.api.dependencies import get_candidate_service, get_current_user
from src.domain.models.candidate import (
    Candidate,
    CandidateCreate,
    CandidateUpdate
)
from src.services.candidate_service import CandidateService

router = APIRouter()


@router.post("/candidates", response_model=Candidate)
async def create_candidate(
    candidate: CandidateCreate,
    service: CandidateService = Depends(get_candidate_service),
    current_user: dict = Depends(get_current_user),
):
    """Create a new candidate."""
    return await service.create_candidate(candidate)


@router.get("/candidates/{candidate_id}", response_model=Candidate)
async def get_candidate(
    candidate_id: str,
    service: CandidateService = Depends(get_candidate_service),
    current_user: dict = Depends(get_current_user),
):
    """Get a candidate by ID."""
    return await service.get_candidate(candidate_id)


@router.put("/candidates/{candidate_id}", response_model=Candidate)
async def update_candidate(
    candidate_id: str,
    candidate: CandidateUpdate,
    service: CandidateService = Depends(get_candidate_service),
    current_user: dict = Depends(get_current_user),
):
    """Update a candidate."""
    return await service.update_candidate(candidate_id, candidate)


@router.delete("/candidates/{candidate_id}")
async def delete_candidate(
    candidate_id: str,
    service: CandidateService = Depends(get_candidate_service),
    current_user: dict = Depends(get_current_user),
):
    """Delete a candidate."""
    await service.delete_candidate(candidate_id)
    return {"status": "success"}


@router.get("/candidates", response_model=dict)
async def search_candidates(
    query: str = "",
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    service: CandidateService = Depends(get_candidate_service),
    current_user: dict = Depends(get_current_user),
):
    """Search candidates with pagination."""
    candidates, total = await service.search_candidates(query, skip, limit)
    return {"items": candidates, "total": total, "skip": skip, "limit": limit}


@router.get("/generate-report")
async def generate_report(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    service: CandidateService = Depends(get_candidate_service),
    current_user: dict = Depends(get_current_user),
):
    """Generate CSV report of all candidates."""
    csv_content = await service.generate_report(skip, limit)
    response = Response(content=csv_content)
    response.headers[
        "Content-Disposition"
    ] = "attachment; filename=candidates.csv"  # noqa: E501
    response.headers["Content-Type"] = "text/csv"
    return response

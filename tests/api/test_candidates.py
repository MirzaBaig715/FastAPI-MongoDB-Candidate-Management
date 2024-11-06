import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_create_candidate(auth_token):
    """Test candidate creation."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/candidates",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "full_name": "John Doe",
                "email": "john@example.com",
                "position": "Software Engineer",
                "experience": 5,
                "skills": ["Python", "FastAPI"],
                "status": "applied"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "John Doe"
        assert "id" in data


@pytest.mark.asyncio
async def test_search_candidates(auth_token):
    """Test candidate search."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First create some test candidates
        candidates = [
            {
                "full_name": "John Doe",
                "email": "john@example.com",
                "position": "Software Engineer",
                "experience": 5,
                "skills": ["Python", "FastAPI"],
                "status": "applied"
            },
            {
                "full_name": "Jane Smith",
                "email": "jane@example.com",
                "position": "Senior Developer",
                "experience": 8,
                "skills": ["Python", "Django"],
                "status": "interviewed"
            }
        ]

        for candidate in candidates:
            await client.post(
                "/api/v1/candidates",
                headers={"Authorization": f"Bearer {auth_token}"},
                json=candidate
            )

        # Test search
        response = await client.get(
            "/api/v1/candidates?query=Python",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["items"]) == 2


@pytest.mark.asyncio
async def test_generate_report(auth_token):
    """Test report generation."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            "/api/v1/generate-report",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "text/csv"
        assert "candidates.csv" in response.headers["Content-Disposition"]

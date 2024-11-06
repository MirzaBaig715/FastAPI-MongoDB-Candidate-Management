from motor.motor_asyncio import AsyncIOMotorClient
from src.config.settings import get_settings

settings = get_settings()


async def create_indexes():
    """Create database indexes."""
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]

    # User indexes
    await db.users.create_index("email", unique=True)

    # Candidate indexes
    await db.candidates.create_index("email", unique=True)
    await db.candidates.create_index([
        ("full_name", "text"),
        ("position", "text"),
        ("skills", "text")
    ])

    client.close()

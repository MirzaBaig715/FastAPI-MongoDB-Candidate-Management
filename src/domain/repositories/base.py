from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

from motor.motor_asyncio import AsyncIOMotorCollection

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    @abstractmethod
    async def create(self, data: T) -> T:
        pass

    @abstractmethod
    async def get(self, id: str) -> Optional[T]:
        pass

    @abstractmethod
    async def update(self, id: str, data: T) -> Optional[T]:
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        pass

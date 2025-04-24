from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Dict, Any

T = TypeVar('T')

class BaseService(ABC):
    """Абстрактный базовый сервис"""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        pass

    @abstractmethod
    def create(self, **kwargs) -> T:
        pass

    @abstractmethod
    def update(self, id: int, **kwargs) -> Optional[T]:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass
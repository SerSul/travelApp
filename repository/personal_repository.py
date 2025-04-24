from entity.models import PersonalData
from .base_repository import BaseRepository
from typing import Type, TypeVar, Optional, List, Dict, Any

class PersonalDataRepository(BaseRepository):
    def __init__(self):
        super().__init__(PersonalData)

    def get_by_full_name(self, first_name: str, last_name: str) -> List[PersonalData]:
        return self.filter_by(first_name=first_name, last_name=last_name)

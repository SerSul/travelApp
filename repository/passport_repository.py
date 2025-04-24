from entity.models import PassportData
from .base_repository import BaseRepository
from typing import Type, TypeVar, Optional, List, Dict, Any

class PassportRepository(BaseRepository):
    def __init__(self):
        super().__init__(PassportData)

    def get_by_employee(self, employee_id: int) -> Optional[PassportData]:
        return self.filter_by(employee_id=employee_id).first()
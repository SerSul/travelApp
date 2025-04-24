from entity.models import Employee
from .base_repository import BaseRepository
from typing import Type, TypeVar, Optional, List, Dict, Any

class EmployeeRepository(BaseRepository):
    def __init__(self):
        super().__init__(Employee)

    def get_active(self) -> List[Employee]:
        return self.filter_by(active=True)

    def get_by_department(self, department_id: int) -> List[Employee]:
        return self.filter_by(department_id=department_id)
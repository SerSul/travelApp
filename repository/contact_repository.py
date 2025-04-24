from entity.models import ContactInfo
from .base_repository import BaseRepository
from typing import Type, TypeVar, Optional, List, Dict, Any

class ContactRepository(BaseRepository):
    def __init__(self):
        super().__init__(ContactInfo)

    def get_by_email(self, email: str) -> Optional[ContactInfo]:
        return self.filter_by(email=email).first()

    def get_by_phone(self, phone: str) -> Optional[ContactInfo]:
        return self.filter_by(phone=phone).first()
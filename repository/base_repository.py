from typing import Type, TypeVar, Optional, List, Dict, Any
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
T = TypeVar('T', bound=db.Model)


class BaseRepository:
    """Базовый CRUD-репозиторий"""

    def __init__(self, model_class: Type[T]):
        self.model = model_class

    def create(self, **kwargs) -> T:
        instance = self.model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

    def get(self, id: int) -> Optional[T]:
        return self.model.query.get(id)

    def get_all(self) -> List[T]:
        return self.model.query.all()

    def update(self, id: int, **kwargs) -> Optional[T]:
        instance = self.get(id)
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            db.session.commit()
        return instance

    def delete(self, id: int) -> bool:
        instance = self.get(id)
        if instance:
            db.session.delete(instance)
            db.session.commit()
            return True
        return False

    def filter_by(self, **filters) -> List[T]:
        return self.model.query.filter_by(**filters).all()
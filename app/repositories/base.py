from typing import Generic, TypeVar, Type, List
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_multi(self, *, skip: int = 0, limit: int = 100, **filters) -> List[ModelType]:
        query = self.db.query(self.model)
        for field, value in filters.items():
            if value is not None:
                query = query.filter(getattr(self.model, field) == value)
        return query.offset(skip).limit(limit).all()

    def create(self, *, obj_in: dict) -> ModelType:
        obj_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
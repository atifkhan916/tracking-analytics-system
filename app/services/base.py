from typing import Generic, TypeVar, Type, List
from fastapi.encoders import jsonable_encoder
from app.repositories.base import BaseRepository

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    def get_multi(
        self, *, skip: int = 0, limit: int = 100, **filters
    ) -> List[ModelType]:
        return self.repository.get_multi(skip=skip, limit=limit, **filters)

    def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        return self.repository.create(obj_in=jsonable_encoder(obj_in))
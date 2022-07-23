from typing import Generic, TypeVar
from project.dao.base import BaseDAO


T = TypeVar('T', bound=BaseDAO)


class BaseService(Generic[T]):
    def __init__(self, dao: T, *args, **kwargs):
        self.dao = dao

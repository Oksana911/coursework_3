from typing import Optional, List

from werkzeug.exceptions import NotFound
from project.dao.base import BaseDAO, T
from project.models import Genre, Director, Movie


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre


class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director


class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie

    def get_fresh(self, page: Optional[int] = None, filter=None) -> List[T]:
        stmt = self._db_session.query(self.__model__)
        if filter:
            stmt = stmt.filter(self.__model__.year >= 2020)
        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()




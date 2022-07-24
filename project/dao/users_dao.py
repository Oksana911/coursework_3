from typing import Optional

from project.dao.base import BaseDAO
from project.models import User, AuthUserSchema


class UsersDAO(BaseDAO[User]):
    __model__ = User

    def get_by_email(self, email: str) -> Optional[AuthUserSchema]:
        user = self._db_session.query(User).filter(User.email == email).one()

        if user is not None:
            return AuthUserSchema().dump(user)
        return None

    def update(self, email, data):
        self._db_session.query(User).filter(User.email == email).update(data)
        self._db_session.commit()
        print('Пользователь обновлен')

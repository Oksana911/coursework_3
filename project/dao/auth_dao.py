from typing import Optional
from project.dao.base import BaseDAO
from project.models import User, AuthUserSchema


class AuthDAO(BaseDAO):

    def register(self, email, password_hash):
        try:
            new_user = User(email=email, password_hash=password_hash)
            self._db_session.add(new_user)
            self._db_session.commit()
            print('Пользователь успешно зарегистрирован')
            return AuthUserSchema().dump(new_user)
        except Exception as e:
            print(e)
            self._db_session.rollback()

    def get_user_by_email(self, email: str) -> Optional[AuthUserSchema]:
        user = self._db_session.query(User).filter(User.email == email).one()

        if user is not None:
            return AuthUserSchema().dump(user)
        return None

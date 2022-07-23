from project.dao.base import BaseDAO
from project.models import User, UserCreatedSchema


class AuthDAO(BaseDAO):

    def register(self, email, password_hash):
        try:
            new_user = User(email=email, password_hash=password_hash)
            self._db_session.add(new_user)
            self._db_session.commit()
            print('Пользователь успешно зарегистрирован')
            return UserCreatedSchema().dump(new_user)
        except Exception as e:
            print(e)
            self._db_session.rollback()


    # def get_token(self, email, password_hash):
    #     try:
    #         stmt = self._db_session.query(self.__model__).filter(self.__model__.email==email).one()
    #         return stmt
    #     except Exception as e:
    #         print(e)
    #         return {}

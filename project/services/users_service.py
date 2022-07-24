from typing import Optional

import jwt
from flask import current_app

from project.dao import UsersDAO
from project.services.base import BaseService
from project.exceptions import ItemNotFound
from project.models import User


class UsersService(BaseService[UsersDAO]):
    def get_item(self, pk: int) -> User:
        if user := self.dao.get_by_id(pk):
            return user
        raise ItemNotFound(f'User with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None) -> list[User]:
        return self.dao.get_all(page=page)

    @staticmethod
    def get_data_from_token(refresh_token):
        data = jwt.decode(jwt=refresh_token, key=current_app.config['JWT_SECRET'], algorithms=current_app.config['JWT_ALGORITHM'])
        return data

    def get_by_token(self, refresh_token):
        data = self.get_data_from_token(refresh_token)

        if data:
            return self.dao.get_by_email(data.get('email'))

    def update_user(self, data, refresh_token):
        user = self.get_by_token(refresh_token)

        if user:
            self.dao.update(email=user.email, data=data)


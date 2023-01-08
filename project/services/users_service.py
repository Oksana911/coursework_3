from typing import Optional, Dict
from project.dao import UsersDAO
from project.services.base import BaseService
from project.exceptions import ItemNotFound
from project.models import User
from project.tools.security import generate_password_hash


class UsersService(BaseService[UsersDAO]):
    def get_item(self, pk: int) -> User:
        if user := self.dao.get_by_id(pk):
            return user
        raise ItemNotFound(f'User with pk={pk} does not exists.')

    def get_all(self, page: Optional[int] = None) -> list[User]:
        return self.dao.get_all(page=page)

    def get_by_token(self, refresh_token) -> User:
        data: Dict = self.get_data_from_token(refresh_token)

        if data:
            return self.dao.get_user_by_email(data['email'])

    def update(self, data, refresh_token):
        user: User = self.get_by_token(refresh_token)

        if user:
            self.dao.update(email=user.email, data=data)
            return user

    def password_update(self, data: Dict, refresh_token):
        user: User = self.get_by_token(refresh_token)

        hash_password = generate_password_hash(data['password_1'])

        if self.compare_passwords(hash_password, user.password_hash):
            user.password_hash = generate_password_hash(data['password_2'])

        self.dao.update_password(user.email, data['password_2'])
        return "Your password was successfully updated"

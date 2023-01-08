import hmac
from typing import Optional, Dict
import jwt
from datetime import datetime, timedelta
from flask import current_app, abort
from project.dao.auth_dao import AuthDAO
from project.exceptions import ItemNotFound, WrongPassword
from project.models import AuthUserSchema, User
from project.services.base import BaseService
from project.tools.security import generate_password_hash


class AuthService(BaseService[AuthDAO]):
    @staticmethod
    def get_hash(password: str):
        return generate_password_hash(password=password)

    @staticmethod
    def __generate_tokens(user_data: Dict) -> Dict:
        if user_data is None:
            raise abort(404)

        payload = {
            'id': user_data['id'],
            'email': user_data['email'],
            'exp': datetime.utcnow() + timedelta(minutes=current_app.config['TOKEN_EXPIRE_MINUTES'])
        }

        access_token = jwt.encode(
            payload=payload,
            key=current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

        # перезаписываем значение payload['exp'] для refresh_token:
        payload['exp'] = datetime.utcnow() + timedelta(days=current_app.config['TOKEN_EXPIRE_DAYS'])

        refresh_token = jwt.encode(
            payload=payload,
            key=current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    def register(self, email: str, password: str) -> AuthUserSchema:
        # хэширует пароль:
        password_hash = self.get_hash(password=password)
        # создает и возвращает юзера:
        new_user = self.dao.register(email=email, password_hash=password_hash)
        return AuthUserSchema().dump(new_user)

    def login(self, email: str, password: str) -> Dict[str, str]:
        user: Optional[User] = self.dao.get_user_by_email(email=email)
        if user is None:
            raise ItemNotFound

        password_hash = self.get_hash(password=password)

        user_data = {
            'id': user.id,
            'email': user.email,

        }
        if not self.compare_passwords(user.password_hash, password_hash):
            raise WrongPassword
        return self.__generate_tokens(user_data)

    def approve_refresh_token(self, refresh_token):
        data = self.get_data_from_token(refresh_token)

        user = self.dao.get_user_by_email(email=data['email'])
        if user is None:
            raise abort(404)

        return self.__generate_tokens(data)

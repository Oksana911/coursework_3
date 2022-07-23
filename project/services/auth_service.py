from project.dao.auth_dao import AuthDAO
from project.models import UserCreatedSchema
from project.services.base import BaseService
from project.tools.security import generate_password_hash


class AuthService(BaseService[AuthDAO]):
    @staticmethod
    def get_hash(password: str):
        return generate_password_hash(password=password)

    # @staticmethod
    # def __get_hash(password: str):
    #     hashed = hashlib.pbkdf2_hmac(
    #         hash_name=current_app.config['HASH_NAME'],
    #         salt=current_app.config['PWD_HASH_SALT'].encode('utf-8'),
    #         iterations=current_app.config['PWD_HASH_ITERATIONS'],
    #         password=password.encode('utf-8'),
    #     )
    #
    #     return base64.b64encode(hashed).decode('utf-8')

    def register(self, email: str, password: str) -> UserCreatedSchema:
        # хэширует пароль:
        password_hash = self.get_hash(password=password)
        # создает и возвращает юзера:
        return self.dao.register(email=email, password_hah=password_hash)

from typing import Generic, TypeVar, Dict
import jwt
from flask import current_app
from flask_restx import abort
from project.dao.base import BaseDAO


T = TypeVar('T', bound=BaseDAO)


class BaseService(Generic[T]):
    def __init__(self, dao: T, *args, **kwargs):
        self.dao = dao

    @staticmethod
    def get_data_from_token(refresh_token) -> Dict:
        user_data = None
        try:
            user_data = jwt.decode(
                jwt=refresh_token,
                key=current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
        except Exception as e:
            print('JWT Decode Error', e)
            abort(401)

        return user_data

from flask import request
from flask_restx import Namespace, Resource

from project.container import user_service
from project.setup.api.models import user

api = Namespace('user')


@api.route('/')
class UserView(Resource):
    @api.marshal_with(user, code=200, description='OK')
    def get(self):
        """ Get user info """
        token = request.headers.environ.get('HTTP_AUTHORIZATION').replace('Bearer ', '')
        return user_service.get_by_token(refresh_token=token)

    @api.marshal_with(user, code=200, description='OK')
    def patch(self):
        """ Update user info """
        data = request.json
        token = request.headers.environ.get('HTTP_AUTHORIZATION').replace('Bearer ', '')

        return user_service.update_user(data=data, refresh_token=token), 201


@api.route('/password')
class UserPasswordView(Resource):
    def put(self):
        """ Update user password """
        pass

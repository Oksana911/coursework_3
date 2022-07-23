from flask import request
from flask_restx import Resource, Namespace
from project.container import auth_service
from project.models import AuthRegisterRequest

api = Namespace('auth')


@api.route('/register/')
class RegisterView(Resource):
    @staticmethod
    def post():
        data = request.json
        validated_data = AuthRegisterRequest().load(data)

        auth_service.register(
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return '', 200


@api.route('/login/')
class LoginView(Resource):
    def post(self):
        pass
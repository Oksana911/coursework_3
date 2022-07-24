from typing import Dict
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
    @staticmethod
    def post():
        data = request.json
        validated_data = AuthRegisterRequest().load(data)

        tokens: Dict[str] = auth_service.login(
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return tokens, 200

    @staticmethod
    def put():
        data = request.json
        refresh_token = data.get("refresh_token")
        if not refresh_token:
            return 'Не задан токен', 400

        tokens = auth_service.approve_refresh_token(refresh_token)

        return tokens, 401


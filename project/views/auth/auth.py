from typing import Dict

from flask import request
from flask_restx import Resource, Namespace
from project.container import auth_service
from project.models import AuthRegisterRequest
from project.setup.api.models import auth
from project.setup.api.models import tokens

api = Namespace('auth')


@api.route('/register/')
class RegisterView(Resource):
    @staticmethod
    @api.expect(auth)
    def post():
        """
        Register new user
        """
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
    @api.response(200, description='Tokens', model=tokens)
    def post():
        """
        Login to get access_token, refresh_token
        """
        data = request.json
        validated_data = AuthRegisterRequest().load(data)

        tokens: Dict[str] = auth_service.login(
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return tokens, 200

    @staticmethod
    @api.response(201, description='Tokens update', model=tokens)
    def put():
        """
        Create and return new tokens
        """
        data = request.json
        refresh_token = data.get("refresh_token")
        if not refresh_token:
            return 'Не задан токен', 400

        tokens = auth_service.approve_refresh_token(refresh_token)

        return tokens, 201

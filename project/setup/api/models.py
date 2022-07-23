from flask_restx import fields, Model

from project.models import GenreSchema, DirectorSchema
from project.setup.api import api

genre: Model = api.model('Жанр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Комедия'),
})

director: Model = api.model('Режиссер', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Иван Иванов'),
})

movie: Model = api.model('Фильм', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True, max_length=100, example='Про Ивана'),
    'description': fields.String(),
    'trailer': fields.String(),
    'year': fields.Integer(),
    'rating': fields.Float(),
    'genre': fields.Nested(genre),
    'director': fields.Nested(director)
})


user: Model = api.model('Пользователь', {
    'id': fields.Integer(required=True, example=1),
    'email': fields.String(required=True, max_length=100, example='example@example.ru'),
    'password': fields.String(),
    'name': fields.String(),
    'surname': fields.Integer(),
    'genre': fields.Nested(genre)
})

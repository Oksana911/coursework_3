from marshmallow import Schema, fields
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from project.setup.db import models


class Genre(models.Base):
    __tablename__ = 'genres'
    name = Column(String(100), unique=True, nullable=False)


class Director(models.Base):
    __tablename__ = 'directors'
    name = Column(String(100), unique=True, nullable=False)


class Movie(models.Base):
    __tablename__ = 'movies'

    title = Column(String(255))
    description = Column(String(255))
    trailer = Column(String(255))
    year = Column(Integer)
    rating = Column(Float)
    genre_id = Column(Integer, ForeignKey(f'{Genre.__tablename__}.id'))
    genre = relationship('Genre')
    director_id = Column(Integer, ForeignKey(f'{Director.__tablename__}.id'))
    director = relationship('Director')


class User(models.Base):
    __tablename__ = 'users'

    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String(255))
    name = Column(String(100))
    surname = Column(String(100))
    favorite_genre = Column(Integer, ForeignKey("genres.id"))


### Схемы для сериализации ###

class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()


class UserSchema(Schema):
    id = fields.Int()
    email = fields.Str()
    password_hash = fields.Str()
    name = fields.Str()
    surname = fields.Str()
    favorite_genre = fields.Int()


class AuthUserSchema(Schema):
    id = fields.Int()
    email = fields.Str(required=True)
    password_hash = fields.Str(required=True)



class AuthRegisterRequest(Schema):  # TODO добавить проверку почты и пароля через @validator
    email = fields.Str(required=True)
    password = fields.Str(required=True)

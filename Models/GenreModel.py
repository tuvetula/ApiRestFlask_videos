import datetime
from flask import abort
from config import db , ma
from sqlalchemy import Table, Column, Integer,ForeignKey,String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_serializer import SerializerMixin

class Genre(db.Model,SerializerMixin):
    serialize_only = ('id','name')

    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), index=True)
    videos = relationship('Video', backref='genre')

    @staticmethod
    def checkGenre(new_genre):
        if isinstance(new_genre,str):
            if new_genre:
                genre = Genre.query.filter(Genre.name==new_genre.strip().capitalize()).one_or_none()
                if genre is None:
                    abort(409,'No genre matches')
                else:
                    return genre.id
            else:
                abort(409,'The field genre is required')
        elif isinstance(new_genre,int):
            genre = Genre.query.filter(Genre.id==new_genre).one_or_none()
            if genre is None:
                abort(409,'No genre matches')
            else:
                return genre.id

    @staticmethod
    def checkNewGenreName(new_genre):
        if isinstance(new_genre,str):
            new_genre = new_genre.strip().capitalize()
            if new_genre:
                return new_genre
            else:
                abort(409,'The field genre is required')
        else:
            abort(409,'The field genre must be a string')
class GenreSchema(ma.SQLAlchemySchema):

    class Meta:

        model = Genre

        sqla_session = db.session

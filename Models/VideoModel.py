import datetime
from config import db, ma , SECRET_KEY, BCRYPT_LOG_ROUNDS
from sqlalchemy_serializer import SerializerMixin
from Models.GenreModel import Genre
from flask import abort


class Video(db.Model, SerializerMixin):
    serialize_only = ('id','name','year','genre_id')

    __tablename__ = 'videos'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), index=True)

    year = db.Column(db.String(10))

    genre_id = db.Column(db.Integer)

    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    @staticmethod
    def checkName(new_name):
        if isinstance(new_name,str):
            if len(new_name.strip()) > 0:
                return new_name.strip().capitalize()
            else:
                abort(409,'The field name is required')
        else:
            abort(409,'The field name must be a string')

    @staticmethod
    def checkYear(new_year):
        if isinstance(new_year,int):
            new_year = str(new_year)
        if isinstance(new_year,str):
            if len(new_year.strip()) == 4:
                return new_year.strip()
            else:
                abort(409,'The field year must contains 4 caracters')
                #return ErrorResponse('The field year must contains 4 caracters',409)
        else:
            abort(409,'The field year must be a string')
            #return ErrorResponse('The field year must be a string',409)
    
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


class VideoSchema(ma.SQLAlchemySchema):

    class Meta:

        model = Video
        sqla_session = db.session



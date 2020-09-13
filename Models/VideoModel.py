import datetime
from config import db, ma , SECRET_KEY, BCRYPT_LOG_ROUNDS
from sqlalchemy import Table, Column, Integer,ForeignKey,DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_serializer import SerializerMixin
from flask import abort

class Video(db.Model, SerializerMixin):
    serialize_only = ('id','name','year','genre_id')

    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), index=True)
    year = Column(String(10))
    genre_id = Column(Integer , ForeignKey('genres.id'))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

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
        else:
            abort(409,'The field year must be a string')


class VideoSchema(ma.SQLAlchemySchema):

    class Meta:

        model = Video
        sqla_session = db.session



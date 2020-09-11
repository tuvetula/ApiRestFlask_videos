from datetime import datetime

from config import db, ma
from sqlalchemy_serializer import SerializerMixin


class Genre(db.Model):

    __tablename__ = 'genres'

    genre_id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), index=True)

class GenreSchema(ma.SQLAlchemySchema):

    class Meta:

        model = Genre

        sqla_session = db.session


class Video(db.Model, SerializerMixin):
    serialize_only = ('id','name','year','genre_id')

    __tablename__ = 'videos'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), index=True)

    year = db.Column(db.String(10))

    genre_id = db.Column(db.Integer)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class VideoSchema(ma.SQLAlchemySchema):

    class Meta:

        model = Video
        sqla_session = db.session
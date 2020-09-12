import datetime
from config import db, ma , SECRET_KEY, BCRYPT_LOG_ROUNDS
from sqlalchemy_serializer import SerializerMixin


class Video(db.Model, SerializerMixin):
    serialize_only = ('id','name','year','genre_id')

    __tablename__ = 'videos'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), index=True)

    year = db.Column(db.String(10))

    genre_id = db.Column(db.Integer)

    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class VideoSchema(ma.SQLAlchemySchema):

    class Meta:

        model = Video
        sqla_session = db.session



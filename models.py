import datetime

from config import db, ma , SECRET_KEY, BCRYPT_LOG_ROUNDS
from sqlalchemy_serializer import SerializerMixin
from config import bcrypt
import jwt


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

    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class VideoSchema(ma.SQLAlchemySchema):

    class Meta:

        model = Video
        sqla_session = db.session


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, BCRYPT_LOG_ROUNDS
        ).decode()
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=60),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token,SECRET_KEY)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

class UserSchema(ma.SQLAlchemySchema):

    class Meta:

        model = User
        sqla_session = db.session

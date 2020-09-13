import datetime
import jwt
from flask import request
from sqlalchemy import Table, Column, Integer,ForeignKey,DateTime, String, Boolean
from config import db , ma, bcrypt, SECRET_KEY, BCRYPT_LOG_ROUNDS, TIME_FOR_TOKEN_DAYS, TIME_FOR_TOKEN_SECONDS
from Models.BlacklistTokensModel import BlacklistToken

class User(db.Model):
    __tablename__ = "users"

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    email = Column(db.String(255), unique=True, nullable=False)
    password = Column(db.String(255), nullable=False)
    registered_on = Column(DateTime, nullable=False)
    admin = Column(Boolean, nullable=False, default=False)

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
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=TIME_FOR_TOKEN_DAYS, seconds=TIME_FOR_TOKEN_SECONDS),
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
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                payload = jwt.decode(auth_token,SECRET_KEY)
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
    
    @staticmethod
    def verifyToken():
        auth_token = request.headers.get('Authorization')
        if auth_token:
            return User.decode_auth_token(auth_token)
        else:
            return 'Provide a auth token'
    
    def verifyPassword(self,hash,password):
        return bcrypt.check_password_hash(hash,password)

class UserSchema(ma.SQLAlchemySchema):

    class Meta:

        model = User
        sqla_session = db.session
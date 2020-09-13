import flask
import config
import Models
import Resources
import Functions
import json
from config import db, app
from Models.GenreModel import Genre, GenreSchema
from Models.VideoModel import Video, VideoSchema
from Models.UserModel import User, UserSchema
from Models.BlacklistTokensModel import BlacklistToken, BlacklistTokenSchema
from Functions.response import successResponse
from Functions.checkMail import checkIfIsValidMailAdress
from Resources.register import UserRegister
from Resources.login import UserLogin
from Resources.logout import UserLogout
from Resources.currentUser import UserCurrentUser
from Resources.videos import Videos
from Resources.videoItem import VideoItem
from Resources.genres import Genres
from Resources.genreItem import GenreItem

from flask import (
    Flask, 
    abort,
    jsonify,
    request
)
from flask_restful_swagger_3 import swagger
from flask_restful_swagger_3 import Api

#app = Flask(__name__)
api = Api(app, version='0.0', api_spec_url='/api')
api.add_resource(UserRegister,'/api/register')
api.add_resource(UserLogin, '/api/login')
api.add_resource(UserLogout, '/api/logout')
api.add_resource(UserCurrentUser, '/api/currentUser')
api.add_resource(Videos, '/api/videos')
api.add_resource(VideoItem, '/api/videos/<int:video_id>')
api.add_resource(Genres, '/api/genres')
api.add_resource(GenreItem, '/api/genres/<int:genre_id>')

app.run()
import flask
import config
import Models
import Functions
import json
from config import db, app
from Models.GenreModel import Genre, GenreSchema
from Models.VideoModel import Video, VideoSchema
from Models.UserModel import User, UserSchema
from Models.BlacklistTokensModel import BlacklistToken, BlacklistTokenSchema
from Functions.response import successResponse
from Functions.checkMail import checkIfIsValidMailAdress

from flask import (
    Flask, 
    abort,
    jsonify,
    request
)



#AUTHENTICATION
#register
@app.route('/api/register', methods=['PUT'])
def register():
    # get the post data
    post_data = request.json
    # check if user already exists
    if 'email' and 'password' in post_data[0]:
        user = User.query.filter_by(email=post_data[0]['email']).first()
        if not user:
            if checkIfIsValidMailAdress(post_data[0]['email']):
                try:
                    new_user = User(
                        email=post_data[0]['email'],
                        password=post_data[0]['password']
                    )
                    # insert the user
                    db.session.add(new_user)
                    db.session.commit()
                    return successResponse(201,'Successfully registered. Log in to obtain a auth_token')
                except Exception as e:
                    user_to_delete = User.query.filter(email=post_data[0]['email']).one_or_none()
                    # delete the user
                    if user_to_delete:
                        db.session.delete(new_user)
                        db.session.commit()
                    abort(401,'Some error occurred. Please try again.')
            else:
                abort(400,'Email adress is not valid.')
        else:
            abort(401,'User already exists. Please Log in.')
    else:
        abort(400,'The request must have an email and password field')

#login
@app.route('/api/login' , methods=['POST'])
def login():
    # get the post data
    post_data = request.json
    # fetch the user data
    if 'email' and 'password' in post_data[0]:
        user = User.query.filter_by(email=post_data[0]['email']).one_or_none()
        if user is not None:
            if user.verifyPassword(user.password,post_data[0]['password']):
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    return successResponse(200,'Successfully logged in.',auth_token.decode())
            else:
                abort(401,'The password is not valid.')
        else:
            abort(401,'No account for this email adress')
    else:
        abort(400,'The request must have an email and password field')

#logout
@app.route('/api/logout' , methods=['POST'])
def logout():
    # get auth token
    resp = User.verifyToken()
    if isinstance(resp, int):
        # mark the token as blacklisted
        BlacklistToken.addTokenInBlacklist(request.headers.get('Authorization'))
        return successResponse(200,'Successfully logged out.')
    else:
        abort(401,resp)

#get user connected
@app.route('/api/currentUser' , methods=['GET'])
def getUserConnected():
    resp = User.verifyToken()
    if isinstance(resp, int):
        user = User.query.filter_by(id=resp).one_or_none()
        if user is not None:
            responseObject = {
                'status': 'success',
                'data': {
                    'user_id': user.id,
                    'email': user.email,
                    'admin': user.admin,
                    'registered_on': user.registered_on
                }
            }
            return jsonify(responseObject)
        else:
            BlacklistToken.addTokenInBlacklist(request.headers.get('Authorization'))
            abort(401,'No account for this request. You have to register.')
    else:
        abort(401,resp)

#VIDEOS
# show list of videos
@app.route('/api/videos' , methods=['GET'])
def index():
        resp = User.verifyToken()
        if not isinstance(resp, str):
            videos = Video.query.order_by(Video.name).all()
            result = []
            for video in videos:
                result.append(video.to_dict())
            return jsonify(result)
        else:
            abort(401,resp)

# create a video
@app.route('/api/videos' , methods=['PUT'])
def create():
    resp = User.verifyToken()
    if isinstance(resp, int):
        if 'name' and 'year' and 'genre' in request.json[0]:
            name = Video.checkName(request.json[0]['name'])
            #On vérifie si une vidéo du même nom existe déjà
            video = Video.query.filter(Video.name == name).one_or_none()
            if video is None:
                year = Video.checkYear(request.json[0]['year'])
                genre = Video.checkGenre(request.json[0]['genre'])
                new_video = Video(name=name,year=year,genre_id=genre)
                #On prépare et enregistre en bdd
                db.session.add(new_video)
                db.session.commit()
                # On récupère la nouvelle entrée en bdd
                new_video_in_DB = Video.query.filter(Video.name == name).one_or_none()
                return new_video_in_DB.to_dict()
            else:
                abort(409,"This movie name already exist")
        else:
            abort(400,"The request must have name, year and genre fields")
    else:
        abort(401,resp)

# Show one video from Videos
@app.route('/api/videos/<int:video_id>' , methods=['GET'])
def show_content_item(video_id):
    resp = User.verifyToken()
    if isinstance(resp, int):
        video = Video.query.filter(Video.id == video_id).one_or_none()
        if video is not None:
            return video.to_dict()
        else:
            abort(404, 'Video not found for id: {video_id}'.format(video_id=video_id))
    else:
        abort(401,resp)

# Update a video
@app.route('/api/videos/<int:video_id>' , methods=['PATCH'])
def update_video(video_id):
    resp = User.verifyToken()
    if isinstance(resp, int):
        video = Video.query.filter(Video.id == video_id).one_or_none()
        if video is None:
            abort(404,'Could not find the video with id: {video_id}'.format(video_id=video_id))
        if 'name' in request.json[0]:
            video.name = Video.checkName(request.json[0]['name'])               
        if 'year' in request.json[0]:
            video.year = Video.checkYear(request.json[0]['year'])               
        if 'genre' in request.json[0]:
            video.genre_id = Video.checkGenre(request.json[0]['genre'])             
        db.session.commit()
        return video.to_dict()
    else:
        abort(401,resp)

@app.route('/api/videos/<int:video_id>' , methods=['DELETE'])
def delete_video(video_id):
    resp = User.verifyToken()
    if isinstance(resp, int):
        video = Video.query.filter(Video.id == video_id).one_or_none()
        if video is None:
            abort(404,"Could not find this video with this id")
        db.session.delete(video)
        db.session.commit()
        return successResponse(200,'The video has been deleted.')
    else:
        abort(401,resp)    

app.run()
    
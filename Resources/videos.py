from flask import Flask, abort, jsonify, request
from config import db
from Functions.response import successResponse
from Models.UserModel import User
from Models.VideoModel import Video
from Models.GenreModel import Genre
from flask_restful import Resource

class Videos(Resource):
    # show list of videos
    def get(self):
        resp = User.verifyToken()
        if isinstance(resp, int):
            videos = Video.query.order_by(Video.name).all()
            if videos:
                result = []
                for video in videos:
                    result.append(video.to_dict())
                return jsonify(result)
            else:
                return successResponse(200,'No videos available')
        else:
            abort(401,resp)

    # create a video
    def put(self):
        resp = User.verifyToken()
        if isinstance(resp, int):
            if 'name' and 'year' and 'genre' in request.json:
                name = Video.checkName(request.json['name'])
                #On vérifie si une vidéo du même nom existe déjà
                video = Video.query.filter(Video.name == name).one_or_none()
                if video is None:
                    year = Video.checkYear(request.json['year'])
                    genre = Genre.checkGenre(request.json['genre'])
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
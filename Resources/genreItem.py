from flask import Flask, abort, jsonify, request
from config import db
from Functions.response import successResponse
from Models.UserModel import User
from Models.GenreModel import Genre
from flask_restful import Resource

class GenreItem(Resource):
    #Voir les vidéos d'un genre
    def get(self,genre_id):
        resp = User.verifyToken()
        if isinstance(resp, int):
            genre = Genre.query.filter(Genre.id == genre_id).one_or_none()
            if genre:
                result = []
                for video in genre.videos:
                    result.append(video.to_dict())
                return jsonify(result)
            else:
                abort(404, 'Genre not found for genre: {genre_id}'.format(genre_id=genre_id))
        else:
            abort(401,resp)
from flask import Flask, abort, jsonify, request
from config import db
from Functions.response import successResponse
from Models.UserModel import User
from Models.GenreModel import Genre
from flask_restful import Resource

class Genres(Resource):
    #Liste des genres
    def get(self):
        resp = User.verifyToken()
        if isinstance(resp, int):
            genres = Genre.query.order_by(Genre.name).all()
            result = []
            for genre in genres:
                result.append(genre.to_dict())
            return jsonify(result)
        else:
            abort(401,resp)

    #Create a genre
    def put(self):
        resp = User.verifyToken()
        if isinstance(resp, int):
            if 'name' in request.json:
                name = Genre.checkNewGenreName(request.json['name'])
                #On vérifie si une vidéo du même nom existe déjà
                genre = Genre.query.filter(Genre.name == name).one_or_none()
                if genre is None:
                    new_genre = Genre(name=name)
                    #On prépare et enregistre en bdd
                    db.session.add(new_genre)
                    db.session.commit()
                    # On récupère la nouvelle entrée en bdd
                    new_genre_in_DB = Genre.query.filter(Genre.name == name).one_or_none()
                    return new_genre_in_DB.to_dict()
                else:
                    abort(409,"This genre name already exist")
            else:
                abort(400,"The request must have a field name")
        else:
            abort(401,resp)

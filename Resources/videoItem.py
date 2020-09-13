from flask import Flask, abort, jsonify, request
from config import db
from Functions.response import successResponse
from Models.UserModel import User
from Models.VideoModel import Video
from Models.GenreModel import Genre
from flask_restful import Resource

class VideoItem(Resource):
    # Show one video from Videos
    def get(self,video_id):
        resp = User.verifyToken()
        if isinstance(resp, int):
            video = Video.query.filter(Video.id == video_id).one_or_none()
            if video:
                return video.to_dict()
            else:
                abort(404, 'Video not found for id: {video_id}'.format(video_id=video_id))
        else:
            abort(401,resp)

    # Update a video
    def patch(self,video_id):
        resp = User.verifyToken()
        if isinstance(resp, int):
            video = Video.query.filter(Video.id == video_id).one_or_none()
            if video is None:
                abort(404,'Could not find the video with id: {video_id}'.format(video_id=video_id))
            if 'name' in request.json:
                video.name = Video.checkName(request.json['name'])               
            if 'year' in request.json:
                video.year = Video.checkYear(request.json['year'])               
            if 'genre' in request.json:
                video.genre_id = Genre.checkGenre(request.json['genre'])             
            db.session.commit()
            return video.to_dict()
        else:
            abort(401,resp)

    #Delete a video
    def delete(self,video_id):
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
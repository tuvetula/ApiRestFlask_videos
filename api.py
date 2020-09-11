import flask
import config
from flask import (
    Flask, 
    make_response,
    abort,
    jsonify,
    request
)
from config import db , app
from models import Video, VideoSchema

#VIDEOS
# show list of videos
@app.route('/api/videos' , methods=['GET'])
def index():
    videos = Video.query.order_by(Video.name).all()
    result = []
    for video in videos:
       content_data = {}
       content_data['id'] = video.id
       content_data['name'] = video.name
       content_data['year'] = video.year
       content_data['genre_id'] = video.genre_id

       result.append(content_data)
    return jsonify(result)

# create a content
@app.route('/api/videos' , methods=['PUT'])
def create():
    #On vérifie si une vidéo du même nom existe déjà
    video = Video.query.filter(Video.name == request.json[0]['name']).one_or_none()
    if video is None:
        name = request.json[0]['name']
        year = request.json[0]['year']
        genre = request.json[0]['genre_id']
        new_video = Video(name=name,year=year,genre_id=genre)
        #On prépare et enregistre en bdd
        db.session.add(new_video)
        db.session.commit()
        # On récupère la nouvelle entrée en bdd
        new_video_in_DB = Video.query.filter(Video.name == name).one_or_none()
        return new_video_in_DB.to_dict()
    else:
        abort(409,"This movie name already exist")


# Show one video from Videos
@app.route('/api/videos/<int:video_id>' , methods=['GET'])
def show_content_item(video_id):
    video = Video.query.filter(Video.id == video_id).one_or_none()
    if video is not None:
        return video.to_dict()
    else:
        abort(404, 'Video not found for id: {video_id}'.format(video_id=video_id))

# Update a video
@app.route('/api/videos/<int:video_id>' , methods=['PATCH'])
def update_video(video_id):
    video = Video.query.filter(Video.id == video_id).one_or_none()
    if video is None:
        abort(404,"Could not find this video with this id: {video_id}")
    if request.json[0]['name']:
        video.name = request.json[0]['name']
    if request.json[0]['year']:
        video.year = request.json[0]['year']
    if request.json[0]['genre_id']:
        video.genre_id = request.json[0]['genre_id']
    db.session.commit()

    return video.to_dict()

@app.route('/api/videos/<int:video_id>' , methods=['DELETE'])
def delete_video(video_id):
    video = Video.query.filter(Video.id == video_id).one_or_none()
    if video is None:
        abort(404,"Could not find this video with this id")
    db.session.delete(video)
    db.session.commit()
    return '',204


app.run()
    
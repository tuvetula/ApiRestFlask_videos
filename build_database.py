import os
from config import db
import Models

from Models import UserModel, BlacklistTokensModel, GenreModel, VideoModel
from Models.GenreModel import Genre
from Models.VideoModel import Video

# Data to initialize database with

CARTOONS = [

    {'name': 'South park', 'year': '1995' , 'genre_id': 1},

    {'name': 'Simpsons', 'year': '1989', 'genre_id': 1},

    {'name': 'American dad','year': '2005', 'genre_id': 1}

]

MOVIES = [
    {'name': 'La haine', 'year': '1995' , 'genre_id': 2},

    {'name': 'Spun', 'year': '2002', 'genre_id': 2},

    {'name': 'Dikkenek','year': '2006', 'genre_id': 2}
]

GENRES = [
    {'name': 'Cartoons'},
    {'name': 'Movies'},
    {'name': 'Series'}
]


# Delete database file if it exists currently

if os.path.exists('database.db'):

    os.remove('database.db')


# Create the database

db.create_all()


# Iterate over the CARTOONS structure and populate the database

for genre in GENRES:
    p = Genre(name=genre['name'])
    db.session.add(p)

for cartoon in CARTOONS:

    p = Video(name=cartoon['name'], year=cartoon['year'], genre_id=cartoon['genre_id'])

    db.session.add(p)

for movie in MOVIES:
    p = Video(name=movie['name'], year=movie['year'], genre_id=movie['genre_id'])

    db.session.add(p)

db.session.commit()
# Modules
    Python 3.8.2
    pip 20.0.2 from /usr/lib/python3/dist-packages/pip (python 3.8)
    Flask 1.1.2
    Werkzeug 1.0.1
    Connexion 2.7.0
    sqlalchemy 1.3.19
    marshmallow 3.7.1
    bcrypt 3.1.7
    json 2.0.9
    jwt 1.7.1
    sqlalchemy_serializer
    flask_apispec 0.10.0




# Documentation Api

# Videos
Les données sont au format json.
[
    {
        'name': string,
        'year': string,
        'genre_id': int
    }
]

GET /api/videos : Pour accéder à l'ensembles des ressources vidéos triées par nom dans l'ordre alphabétique.

GET /api/videos/{id} : Pour accéder à une vidéo. Le paramètre id doit être un nombre entier.

PUT /api/videos : Permet de créer une nouvelle vidéo. La requête doit être envoyée au format json.[{'name' : 'string' , 'year': 'string' , 'genre':'int'}]

PATCH /api/videos/{id} : Permet de mettre à jour une vidéo. La requête doit être envoyée au format json. Le paramètre id doit être un nombre entier.

DELETE /api/videos/{id} : Permet de supprimer une vidéo.Le paramètre id doit être un nombre entier.
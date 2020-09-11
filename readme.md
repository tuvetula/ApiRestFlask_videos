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
# Documentation Api
Les données sont au format json.

# Authentication
PUT /api/register : Pour créer un compte.
    Response: 201
        {
            "detail": "Successfully registered. Log in to obtain a auth_token",
            "status": 201,
            "title": "Success"
        }

POST /api/login : Pour se connecter.
    Response: 200
        {
            "detail": "Successfully logged in.",
            "status": 200,
            "title": "Success",
            "auth_token": "token"
        }

    Token expire après 10 minutes. Il faut se reconnecter pour obtenir un nouveau token.

GET /api/currentUser : Permet d'obtenir les informations de l'utilisateur connecté.
    Response: 200
        {
            "data": {
                "admin": false,
                "email": "test6@test.com",
                "registered_on": "2020-09-13T21:23:44.887768Z",
                "user_id": 1
            },
            "status": "success"
        }

POST /api/logout : Permet de se déconnecter. Le token utilisé pour se déconnecter est  ensuite blacklisté et devient donc inutilisable.
    Response: 200
        {
            "detail": "Successfully logged out.",
            "status": 200,
            "title": "Success"
        }

# VIDEOS
Pour avoir accès aux vidéos, un token valide dans le header doit être fourni.
    Authorization: Token

# List of videos
GET /api/videos : Pour accéder à l'ensemble des ressources vidéos triées par nom dans l'ordre alphabétique.
    Response: 200
        Retourne une liste de videos:
            [
                {
                    "genre_id": 1,
                    "id": 3,
                    "name": "American dad",
                    "year": "2005"
                }
            ]

# Create a video
PUT /api/videos : Permet de créer une nouvelle vidéo. La requête doit être envoyée au format json:
        {
            'name': string,
            'year': string or int, 4 caracters
            'genre_id': string or int. Doit correspondre à un genre existant
        }
    Response: 200
        Retourne la vidéo créé
        {
            "year": "1989",
            "genre_id": 3,
            "id": 7,
            "name": "Le péril jeune"
        }

# Get one video
GET /api/videos/{id} : Pour accéder à une vidéo. Le paramètre id doit être un nombre entier.
    Response: 200
        {
            "year": "1995",
            "genre_id": 1,
            "id": 1,
            "name": "South park"
        }

# Update a video
PATCH /api/videos/{id} : Permet de mettre à jour une vidéo. La requête doit être envoyée au format json. Le paramètre id doit être un nombre entier.
    {
        'name': string,
        'year': string or int, 4 caracters
        'genre_id': string or int. Doit correspondre à un genre existant
    }
    Response: 200
        {
            "year": "1990",
            "genre_id": 3,
            "id": 7,
            "name": "Le grand splash"
        }

# Delete a video
DELETE /api/videos/{id} : Permet de supprimer une vidéo.Le paramètre id doit être un nombre entier.
    Response: 200
        {
            "detail": "The video has been deleted.",
            "status": 200,
            "title": "Success"
        }

# GENRES
Pour avoir accès aux genres, un token valide dans le header doit être fourni.
    Authorization: Token

# Get list of genres
GET /api/genres : Permet d'obtenir la liste des genres.
    Response: 200
        [
            {
                "id": 1,
                "name": "Cartoons"
            }
        ]

# Create a new genre
PUT /api/genres : Permet de créer un nouveau genre. Retourne le genre créé
    Response: 200
        {
            "name": "Manga",
            "id": 4
        }

# Get list of videos from one genre
GET /api/genres/{id} : Permet d'obtenir la liste des videos apparatenant à un genre. Le paramètre id doit être un nombre entier correspondant à l'id d'un genre.
    Response: 200
        [
            {
                "genre_id": 2,
                "id": 4,
                "name": "La haine",
                "year": "1995"
            }
        ]
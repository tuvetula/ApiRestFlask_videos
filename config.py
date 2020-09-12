import os
import connexion
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

basedir = os.path.abspath(os.path.dirname(__file__))

# Create the Connexion application instance

connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance

app = connex_app.app
bcrypt = Bcrypt(app)

# Configure the SQLAlchemy part of the app instance

app.config['SQLALCHEMY_ECHO'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(basedir, 'database.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["DEBUG"] = True

# Create the SQLAlchemy db instance

db = SQLAlchemy(app)

# Initialize Marshmallow

ma = Marshmallow(app)

SECRET_KEY="\xb3\x88e\x0e\xab\xa93\x01x\x82\xd1\xe0\x1b\xb6f;\x1a\x91d\x91\xc1-I\x00"
BCRYPT_LOG_ROUNDS = 13
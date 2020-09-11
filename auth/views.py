# project/server/auth/views.py

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from config import bcrypt, db
from models import User

auth_blueprint = Blueprint('auth', __name__)

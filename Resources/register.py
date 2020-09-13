from flask import Flask, abort, jsonify, request
from config import db
from Functions.checkMail import checkIfIsValidMailAdress
from Functions.response import successResponse
from Models.BlacklistTokensModel import BlacklistToken, BlacklistTokenSchema
from Models.UserModel import User, UserSchema
from flask_restful import Resource

class UserRegister(Resource):
    def put(self):
        # get the post data
        post_data = request.json
        # check if user already exists
        if 'email' and 'password' in post_data[0]:
            user = User.query.filter_by(email=post_data[0]['email']).first()
            if not user:
                if checkIfIsValidMailAdress(post_data[0]['email']):
                    try:
                        new_user = User(
                            email=post_data[0]['email'],
                            password=post_data[0]['password']
                        )
                        # insert the user
                        db.session.add(new_user)
                        db.session.commit()
                        return successResponse(201,'Successfully registered. Log in to obtain a auth_token')
                    except Exception as e:
                        user_to_delete = User.query.filter(email=post_data[0]['email']).one_or_none()
                        # delete the user
                        if user_to_delete:
                            db.session.delete(new_user)
                            db.session.commit()
                        abort(401,'Some error occurred. Please try again.')
                else:
                    abort(400,'Email adress is not valid.')
            else:
                abort(401,'User already exists. Please Log in.')
        else:
            abort(400,'The request must have an email and password field')

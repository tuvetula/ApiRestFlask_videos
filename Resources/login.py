from flask import Flask, abort, jsonify, request
from Functions.response import successResponse
from Models.UserModel import User, UserSchema
from flask_restful import Resource

class UserLogin(Resource):
    def post(self):
        # get the post data
        post_data = request.json
        # fetch the user data
        if 'email' and 'password' in post_data[0]:
            user = User.query.filter_by(email=post_data[0]['email']).one_or_none()
            if user:
                if user.verifyPassword(user.password,post_data[0]['password']):
                    auth_token = user.encode_auth_token(user.id)
                    if auth_token:
                        return successResponse(200,'Successfully logged in.',auth_token.decode())
                else:
                    abort(401,'The password is not valid.')
            else:
                abort(401,'No account for this email adress')
        else:
            abort(400,'The request must have an email and password field')
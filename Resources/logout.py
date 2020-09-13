from flask import Flask, abort, jsonify, request
from Functions.response import successResponse
from Models.UserModel import User, UserSchema
from Models.BlacklistTokensModel import BlacklistToken
from flask_restful import Resource

class UserLogout(Resource):
    def post(self):
        resp = User.verifyToken()
        if isinstance(resp, int):
            # mark the token as blacklisted
            BlacklistToken.addTokenInBlacklist(request.headers.get('Authorization'))
            return successResponse(200,'Successfully logged out.')
        else:
            abort(401,resp)
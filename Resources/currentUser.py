from flask import Flask, abort, jsonify
from Models.UserModel import User
from Models.BlacklistTokensModel import BlacklistToken
from flask_restful import Resource

class UserCurrentUser(Resource):
    #get user connected
    def get(self):
        resp = User.verifyToken()
        if isinstance(resp, int):
            user = User.query.filter_by(id=resp).one_or_none()
            if user is not None:
                responseObject = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                        'admin': user.admin,
                        'registered_on': user.registered_on
                    }
                }
                return jsonify(responseObject)
            else:
                BlacklistToken.addTokenInBlacklist(request.headers.get('Authorization'))
                abort(401,'No account for this request. You have to register.')
        else:
            abort(401,resp)

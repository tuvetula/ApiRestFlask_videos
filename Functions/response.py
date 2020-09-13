import flask
from flask import jsonify

def successResponse(statusCode,message,token=None):
    response = {
        'detail': message,
        'status': statusCode,
        'title': 'Success'
    }
    if token:
        response['auth_token'] = token

    return jsonify(response),statusCode

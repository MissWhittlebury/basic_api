from http import HTTPStatus

from flask import jsonify
from flask_httpauth import HTTPTokenAuth

from api.models import User


token_auth = HTTPTokenAuth()


@token_auth.verify_token
def verify_token(token):
    user_row = None
    if token:
        user_row = User.query.filter_by(token=token).first()
    return user_row is not None


@token_auth.error_handler
def token_auth_error():
    return jsonify({'message': 'unauthorized or non-existent token'}), \
           HTTPStatus.UNAUTHORIZED.value

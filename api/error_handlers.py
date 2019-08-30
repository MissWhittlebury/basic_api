from http import HTTPStatus

from flask import jsonify
from flask_cors import cross_origin


@cross_origin()
def handle_404(e):
    return jsonify({'message': 'url cannot be found'}), \
           HTTPStatus.NOT_FOUND.value

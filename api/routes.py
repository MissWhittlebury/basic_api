from http import HTTPStatus

from flask import Blueprint, request, jsonify
from flask_cors import CORS

from api import db
from api.auth import token_auth
from api.models import User, Item


bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return jsonify({'message': 'service up'}), HTTPStatus.OK.value


@bp.route('/collection', methods=['POST'])
@token_auth.login_required
def collection():
    if not request.json or not request.json.get('email').strip():
        return jsonify({'message': 'email is a required field'}), \
               HTTPStatus.BAD_REQUEST.value
    data = request.json
    if Item.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'email already exists'}), \
               HTTPStatus.BAD_REQUEST.value
    token = request.headers.get('Authorization').replace('Bearer ', '')
    user = User.query.filter_by(token=token).first()
    item = Item(email=data['email'], name=data['name'], user_id=user.id)
    db.session.add(item)
    db.session.commit()
    return jsonify({'id': item.id}), HTTPStatus.CREATED.value


@bp.route('/item/<item_id>', methods=['GET', 'POST'])
@token_auth.login_required
def item(item_id):
    item = Item.query.filter_by(id=item_id).first()
    if item is None:
        return jsonify({'message': 'item does not exist'}), \
               HTTPStatus.NOT_FOUND.value

    token = request.headers.get('Authorization').replace('Bearer ', '')
    if not item.user_authorized(token):
        return jsonify({'message': 'toekn not authorized to access item'}), \
               HTTPStatus.FORBIDDEN.value
    if request.method == 'POST':
        if not request.json or not request.json.get('name').strip():
            return jsonify({'message': 'name is a required field for update'}), \
                   HTTPStatus.BAD_REQUEST.value
        item.name = request.json['name']
        db.session.add(item)
        db.session.commit()
        return jsonify({'message': 'name of item successfully updated'}), \
               HTTPStatus.OK.value

    return jsonify(item.to_dict()), HTTPStatus.OK.value

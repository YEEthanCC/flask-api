from flask import Blueprint
from flask import request, make_response
from app.controllers import *
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager
from app import app


user = Blueprint('user', __name__)
jwt = JWTManager(app)

@user.route('/', methods=['GET'])
@jwt_required()
def list_users_route():
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({'message': 'Token is missing!'})
    return get_all_users()

@user.route('/search', methods=['GET'])
@jwt_required()
def search_user_route():
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({'message': 'Token is missing!'})
    data = request.get_json()
    return get_users_by_name(data['fullname'])

@user.route('/<public_id>', methods=['GET'])
@jwt_required()
def get_user_route(public_id):
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({'message': 'Token is missing!'})
    return get_user(public_id)


@user.route('/signup', methods=['POST'])
def signup_route():
    data = request.get_json()
    return create_user(data['fullname'], data['pwd'])

@user.route('/signin', methods=['POST'])
def signin_route():
    data = request.get_json()
    if not data or not data['fullname'] or not data['pwd']:
        return jsonify({'message': 'Missing username or password'})
    user_id = get_public_id(data['fullname'], data['pwd'])
    if not user_id:
        return jsonify({'message': 'Incorrect username or password'})
    return jsonify(access_token=create_access_token(identity=user_id))

@user.route('/<public_id>', methods=['DELETE'])
@jwt_required()
def delete_user_route(public_id):
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({'message': 'Token is missing!'})
    return delete_user(public_id)

@user.route('/<public_id>', methods=['PUT'])
@jwt_required()
def update_user_route(public_id):
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({'message': 'Token is missing!'})
    data = request.get_json()
    return udpate_user(public_id, data['fullname'], data['pwd'])

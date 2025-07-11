from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity, get_jwt
)
from app.core.jwt import jwt_blacklist  # Import blacklist from core

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # Replace with real authentication logic
    if username == 'admin' and password == 'password':
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify({'msg': 'Bad credentials'}), 401

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    jwt_blacklist.add(jti)
    return jsonify({'msg': 'Successfully logged out'}), 200

@auth_bp.route('/welcome', methods=['GET'])
@jwt_required()
def welcome():
    current_user = get_jwt_identity()
    return jsonify({'msg': f'You are logged in as {current_user}'}), 200
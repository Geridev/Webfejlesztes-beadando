from flask import Blueprint, request, jsonify
from app import db, bcrypt
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], email=data['email'], password_hash=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="User registered successfully"), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password_hash, data['password']):
        token = create_access_token(identity={'id': user.id, 'role': user.role})
        return jsonify(token=token), 200
    return jsonify(error="Invalid credentials"), 401


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # With JWT, you normally handle logout on the frontend by deleting the token.
    # Optionally, you could add token blacklisting here.
    current_user = get_jwt_identity()
    return jsonify(message=f"User {current_user['id']} logged out successfully"), 200

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from extensions import db, bcrypt
from models import User

user_bp = Blueprint('users', __name__)

# 🟢 Get all users (Admin only)
@user_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify(error="Admins only"), 403
    users = User.query.all()
    return jsonify([
        {"id": u.id, "username": u.username, "email": u.email, "role": u.role}
        for u in users
    ]), 200


# 🟢 Get single user by ID (Admin or self)
@user_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()
    user = User.query.get_or_404(id)
    if claims['role'] != 'admin' and current_user_id != user.id:
        return jsonify(error="Not authorized"), 403
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    }), 200


# 🟡 Update user info (Admin or self)
@user_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()
    user = User.query.get_or_404(id)

    if claims['role'] != 'admin' and current_user_id != user.id:
        return jsonify(error="Not authorized"), 403

    data = request.get_json()
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']

    # Allow password change
    if 'password' in data:
        user.password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    # Admins can promote/demote users
    if claims['role'] == 'admin' and 'role' in data:
        user.role = data['role']

    db.session.commit()
    return jsonify(message="User updated successfully"), 200


# 🔴 Delete user (Admin only)
@user_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify(error="Admins only"), 403

    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(message=f"User {user.username} deleted successfully"), 200

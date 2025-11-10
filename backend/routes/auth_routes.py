from flask import Blueprint, request, jsonify
from extensions import db, bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from models import User, RevokedToken

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not all(k in data for k in ('username', 'email', 'password')):
        return jsonify(error="Missing required fields"), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify(error="Username already taken"), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify(error="Email already registered"), 400

    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], email=data['email'], password_hash=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(message="User registered successfully"), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify(error="Missing username or password"), 400

    user = User.query.filter_by(username=data['username']).first()

    if user and bcrypt.check_password_hash(user.password_hash, data['password']):
        token = create_access_token(
            identity=str(user.id),
            additional_claims={"role": user.role}
        )
        user = {"id": user.id, "username": user.username, "email": user.email, "role": user.role}
        return jsonify(access_token=token, user=user), 200

    return jsonify(error="Invalid credentials"), 401


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]  # get unique token identifier
    db.session.add(RevokedToken(jti=jti))
    db.session.commit()
    current_user_id = get_jwt_identity()
    return jsonify(message=f"User {current_user_id} logged out successfully"), 200

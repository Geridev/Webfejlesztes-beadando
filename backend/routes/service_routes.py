from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Service

service_bp = Blueprint('services', __name__)

@service_bp.route('/', methods=['GET'])
def get_services():
    services = Service.query.all()
    result = []
    for s in services:
        result.append({
            "id": s.id,
            "name": s.name,
            "description": s.description,
            "duration": s.duration,
            "price": s.price
        })
    return jsonify(result), 200


@service_bp.route('/', methods=['POST'])
@jwt_required()
def add_service():
    user = get_jwt_identity()
    if user['role'] != 'admin':
        return jsonify(error="Admins only"), 403
    data = request.get_json()
    new_service = Service(**data)
    db.session.add(new_service)
    db.session.commit()
    return jsonify(message="Service added"), 201


@service_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_service(id):
    user = get_jwt_identity()
    if user['role'] != 'admin':
        return jsonify(error="Admins only"), 403

    data = request.get_json()
    service = Service.query.get_or_404(id)
    service.name = data.get('name', service.name)
    service.description = data.get('description', service.description)
    service.duration = data.get('duration', service.duration)
    service.price = data.get('price', service.price)
    db.session.commit()
    return jsonify(message="Service updated"), 200


@service_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_service(id):
    user = get_jwt_identity()
    if user['role'] != 'admin':
        return jsonify(error="Admins only"), 403

    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    return jsonify(message="Service deleted"), 200

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from extensions import db
from models import Appointment

appointment_bp = Blueprint('appointments', __name__)

@appointment_bp.route('/', methods=['GET'])
@jwt_required()
def get_appointments():
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()
    if claims['role'] == 'admin':
        appointments = Appointment.query.all()
    else:
        appointments = Appointment.query.filter_by(user_id=current_user_id).all()
    
    result = []
    for a in appointments:
        result.append({
            "id": a.id,
            "user_id": a.user_id,
            "service_id": a.service_id,
            "datetime": a.datetime,
            "status": a.status
        })
    return jsonify(result), 200


@appointment_bp.route('/', methods=['POST'])
@jwt_required()
def create_appointment():
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    new_appointment = Appointment(
        user_id=current_user_id,
        service_id=data['service_id'],
        datetime=data['datetime'],
        status='booked'
    )
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify(message="Appointment created"), 201


@appointment_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_appointment(id):
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()
    data = request.get_json()
    appointment = Appointment.query.get_or_404(id)

    # Users can only edit their own appointments
    if claims['role'] != 'admin' and appointment.user_id != current_user_id:
        return jsonify(error="Not authorized"), 403

    appointment.datetime = data.get('datetime', appointment.datetime)
    appointment.status = data.get('status', appointment.status)
    db.session.commit()
    return jsonify(message="Appointment updated"), 200


@appointment_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_appointment(id):
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()
    appointment = Appointment.query.get_or_404(id)

    # Users can only delete their own appointments
    if claims['role'] != 'admin' and appointment.user_id != current_user_id:
        return jsonify(error="Not authorized"), 403

    db.session.delete(appointment)
    db.session.commit()
    return jsonify(message="Appointment deleted"), 200

# app.py
from flask import Flask, jsonify
from extensions import db, bcrypt, jwt, cors
from models import RevokedToken

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    from routes.auth_routes import auth_bp
    from routes.user_routes import user_bp
    from routes.service_routes import service_bp
    from routes.appointment_routes import appointment_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(service_bp, url_prefix='/api/services')
    app.register_blueprint(appointment_bp, url_prefix='/api/appointments')

    with app.app_context():
        db.create_all()

    # ✅ Token blacklist check using the database
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return db.session.query(RevokedToken.id).filter_by(jti=jti).scalar() is not None

    # ✅ Response for revoked tokens
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify(error="Token has been revoked"), 401

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

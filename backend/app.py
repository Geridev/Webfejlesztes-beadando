from flask import Flask
from extensions import db, bcrypt, jwt, cors

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    # Import routes *after* app + extensions initialized
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

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

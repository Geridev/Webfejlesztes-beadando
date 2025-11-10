from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # change in production

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)  # Allow React frontend

from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.service_routes import service_bp
from routes.appointment_routes import appointment_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(service_bp, url_prefix='/api/services')
app.register_blueprint(appointment_bp, url_prefix='/api/appointments')

if __name__ == '__main__':
    app.run(debug=True)

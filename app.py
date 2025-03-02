from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.user import user_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS: allow requests from your React app running on localhost:5173
    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)

    # Default route
    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to GymManager API!"})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=5000)

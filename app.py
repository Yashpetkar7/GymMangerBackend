# app.py
from flask import Flask, jsonify
from flask_cors import CORS
from extensions import users_collection  # Now imported from extensions.py

app = Flask(__name__)
CORS(app)

# Register the blueprint from routes/user.py

# Import and register blueprints
from routes.auth import auth_bp
from routes.user import user_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(user_bp, url_prefix='/api/user')

# API Test Route
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Gym Management API is Running"}), 200

if __name__ == '__main__':
    app.run(debug=True)

# routes/auth.py
from flask import Blueprint, request, jsonify
from extensions import users_collection  # Import shared DB resource
from bson.objectid import ObjectId

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    # Now checking for 'username' and 'password'
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"authorized": False, "error": "Missing username or password"}), 400

    # Find the user by username
    user = users_collection.find_one({"username": data["username"]})
    
    # For production, always use hashed passwords
    if user and user.get("password") == data["password"]:
        return jsonify({
            "authorized": True,
            "user_id": str(user["_id"]),
            "role": user.get("role", "user")
        }), 200
    else:
        return jsonify({
            "authorized": False,
            "error": "Invalid credentials"
        }), 401

# # routes/auth.py
# from flask import Blueprint, request, jsonify
# from extensions import users_collection  # Import shared DB resource
# from bson.objectid import ObjectId

# auth_bp = Blueprint('auth_bp', __name__)

# @auth_bp.route('/login', methods=['POST'])
# def login():
#     data = request.json
#     # Now checking for 'username' and 'password'
#     if not data or 'username' not in data or 'password' not in data:
#         return jsonify({"authorized": False, "error": "Missing username or password"}), 400

#     # Find the user by username
#     user = users_collection.find_one({"username": data["username"]})
    
#     # For production, always use hashed passwords
#     if user and user.get("password") == data["password"]:
#         return jsonify({
#             "authorized": True,
#             "user_id": str(user["_id"]),
#             "role": user.get("role", "user")
#         }), 200
#     else:
#         return jsonify({
#             "authorized": False,
#             "error": "Invalid credentials"
#         }), 401
# backend/routes/auth.py
from flask import Blueprint, request, jsonify
from utils.db import db
from datetime import datetime

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')  # Assume it is hashed on the client or compare after hashing

    user = db.users.find_one({"username": username})
    if user and user.get("password") == password:
        # Concatenate firstName and lastName to form fullName
        fullName = f"{user['personalDetails'].get('firstName', '')} {user['personalDetails'].get('lastName', '')}"
        # For simplicity, return user id (you can implement JWT later)
        return jsonify({
            "success": True,
            "token": str(user["_id"]),  # using _id as token
            "role": user["role"],
            "userId": str(user["_id"]),
            "fullName": fullName
        })
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401


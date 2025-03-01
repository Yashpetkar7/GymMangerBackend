# routes/user.py
from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from extensions import users_collection  # Import shared resource from extensions.py

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/register', methods=['POST'])
def register_user():
    data = request.json
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    user = {
        "fullName": data.get("fullName"),
        "email": data["email"],
        "password": data["password"],  # For production, hash the password!
        "role": "user",
        "subscription": data.get("subscription", {}),
        "qrCode": "",
        "bookings": [],
        "complaints": []
    }

    inserted_id = users_collection.insert_one(user).inserted_id
    return jsonify({"message": "User registered successfully", "user_id": str(inserted_id)}), 201

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = users_collection.find()
    user_list = []
    for user in users:
        user["_id"] = str(user["_id"])
        user_list.append(user)
    return jsonify(user_list), 200

@user_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = str(user["_id"])
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

@user_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted successfully"}), 200

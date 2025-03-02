# backend/routes/admin.py
from flask import Blueprint, request, jsonify
from utils.db import db
from bson.objectid import ObjectId
from datetime import datetime

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/api/admin/users', methods=['GET'])
def get_all_users():
    users = list(db.users.find())
    # Convert ObjectId to string
    for user in users:
        user["_id"] = str(user["_id"])
    return jsonify(users)

@admin_bp.route('/api/admin/users', methods=['POST'])
def create_user():
    data = request.get_json()
    data["createdAt"] = datetime.utcnow()
    data["updatedAt"] = datetime.utcnow()
    result = db.users.insert_one(data)
    return jsonify({"message": "User created", "userId": str(result.inserted_id)}), 201

@admin_bp.route('/api/admin/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    data["updatedAt"] = datetime.utcnow()
    result = db.users.update_one({"_id": ObjectId(user_id)}, {"$set": data})
    if result.matched_count:
        return jsonify({"message": "User updated"})
    else:
        return jsonify({"message": "User not found"}), 404

@admin_bp.route('/api/admin/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = db.users.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count:
        return jsonify({"message": "User deleted"})
    else:
        return jsonify({"message": "User not found"}), 404

@admin_bp.route('/api/admin/requests', methods=['GET'])
def get_all_requests():
    requests_list = list(db.requests.find())
    for req in requests_list:
        req["_id"] = str(req["_id"])
        req["userId"] = str(req["userId"])
    return jsonify(requests_list)

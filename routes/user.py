# # routes/user.py
# from flask import Blueprint, request, jsonify
# from bson.objectid import ObjectId
# from extensions import users_collection  # Import shared resource from extensions.py

# user_bp = Blueprint('user_bp', __name__)

# @user_bp.route('/register', methods=['POST'])
# def register_user():
#     data = request.json
#     if not data or 'email' not in data or 'password' not in data:
#         return jsonify({"error": "Missing required fields"}), 400

#     user = {
#         "fullName": data.get("fullName"),
#         "email": data["email"],
#         "password": data["password"],  # For production, hash the password!
#         "role": "user",
#         "subscription": data.get("subscription", {}),
#         "qrCode": "",
#         "bookings": [],
#         "complaints": []
#     }

#     inserted_id = users_collection.insert_one(user).inserted_id
#     return jsonify({"message": "User registered successfully", "user_id": str(inserted_id)}), 201

# @user_bp.route('/users', methods=['GET'])
# def get_users():
#     users = users_collection.find()
#     user_list = []
#     for user in users:
#         user["_id"] = str(user["_id"])
#         user_list.append(user)
#     return jsonify(user_list), 200

# @user_bp.route('/users/<user_id>', methods=['GET'])
# def get_user(user_id):
#     user = users_collection.find_one({"_id": ObjectId(user_id)})
#     if user:
#         user["_id"] = str(user["_id"])
#         return jsonify(user), 200
#     return jsonify({"error": "User not found"}), 404

# @user_bp.route('/users/<user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     result = users_collection.delete_one({"_id": ObjectId(user_id)})
#     if result.deleted_count == 0:
#         return jsonify({"error": "User not found"}), 404
#     return jsonify({"message": "User deleted successfully"}), 200
# backend/routes/user.py
from flask import Blueprint, request, jsonify
from utils.db import db
from bson.objectid import ObjectId
from datetime import datetime

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/api/user/profile', methods=['GET'])
def get_profile():
    # Simulate authentication: get user id from query or local storage (passed by client)
    user_id = request.args.get('userId')
    user = db.users.find_one({"_id": ObjectId(user_id)}, {"password": 0})
    if user:
        # Return only the profile related fields
        profile = {
            "personalDetails": user.get("personalDetails", {}),
            "healthDetails": user.get("healthDetails", {}),
            "membership": user.get("membership", {}),
            "trainingProgram": user.get("trainingProgram", "")
        }
        return jsonify(profile)
    else:
        return jsonify({"message": "User not found"}), 404

@user_bp.route('/api/user/requests', methods=['POST'])
def create_request():
    data = request.get_json()
    data["createdAt"] = datetime.utcnow()
    data["updatedAt"] = datetime.utcnow()
    result = db.requests.insert_one(data)
    return jsonify({"message": "Request created", "requestId": str(result.inserted_id)}), 201

@user_bp.route('/api/user/requests', methods=['GET'])
def get_user_requests():
    user_id = request.args.get('userId')
    requests_list = list(db.requests.find({"userId": ObjectId(user_id)}))
    for req in requests_list:
        req["_id"] = str(req["_id"])
        req["userId"] = str(req["userId"])
    return jsonify(requests_list)

@user_bp.route('/api/user/meals', methods=['GET'])
def get_meals():
    meals = list(db.meals.find({"available": True}))
    for meal in meals:
        meal["_id"] = str(meal["_id"])
    return jsonify(meals)

@user_bp.route('/api/user/meals/orders', methods=['GET'])
def get_meal_orders():
    # Assuming there is a separate collection for meal orders; if orders are part of requests, adjust accordingly.
    user_id = request.args.get('userId')
    orders = list(db.meal_orders.find({"userId": ObjectId(user_id)}))
    for order in orders:
        order["_id"] = str(order["_id"])
        order["userId"] = str(order["userId"])
    return jsonify(orders)

@user_bp.route('/api/user/meals/orders', methods=['POST'])
def book_meal_order():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    # Validate required fields (simplified validation)
    required_fields = ['userId', 'bookingDate', 'selectedMeals']
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"Missing field: {field}"}), 400

    # Convert bookingDate from ISO format to a datetime object
    try:
        # Replace 'Z' with '+00:00' for proper parsing if needed.
        data["bookingDate"] = datetime.fromisoformat(data["bookingDate"].replace("Z", "+00:00"))
    except Exception as e:
        return jsonify({"message": "Invalid bookingDate format"}), 400

    # Optionally, add createdAt timestamp
    data["createdAt"] = datetime.utcnow()

    # Insert the meal order document into the meal_orders collection
    result = db.meal_orders.insert_one(data)

    return jsonify({
        "message": "Meal order booked successfully",
        "orderId": str(result.inserted_id)
    }), 201
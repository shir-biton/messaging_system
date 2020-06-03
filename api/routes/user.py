from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

from models.user import User

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/api/v1/users", methods=["POST"])
def create_user():
    data = request.get_json()
    user = User(**data)

    try:
        user.save()
        return make_response(jsonify(user))
    except Exception as e:
        return make_response(jsonify({"error": str(e)}))

@user_bp.route("/api/v1/users/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return make_response(jsonify({"error": "Missing JSON in request"}), 400)

    user = User.objects.get(email=data.get("email"))
    
    if not user:
        return make_response(jsonify({"error": "Could not verify"}), 401)
    
    try:
        user.check_pw_hash(data.get('password'))        
    except ValueError:
        return make_response(jsonify({"error": "Could not verify"}), 401)

    access_token = create_access_token(identity=str(user.id))
    return make_response(jsonify(access_token=access_token), 200)

@user_bp.route("/api/v1/users/me", methods=["GET"])
@jwt_required
def get_user():
    current_user = get_jwt_identity()
    return make_response(jsonify(logged_in_as=current_user), 200)
import datetime
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token

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
        return make_response(jsonify({"error": str(e)}), 500)

@user_bp.route("/api/v1/users/login", methods=["POST"])
def login():
    """
    Validates user credentials. Returns access token and user details or an error message.
    """
    data = request.get_json()

    if not data:
        return make_response(jsonify({"error": "Missing JSON in request"}), 400)

    try:
        user = User.objects(email=data.get("email"))
        
        if not user:
            return make_response(jsonify({"error": "Could not verify"}), 401)

        user = user.first()
        
        try:
            user.check_pw_hash(data.get('password'))        
        except ValueError:
            return make_response(jsonify({"error": "Could not verify"}), 401)

        access_token = create_access_token(identity=str(user.id), expires_delta=datetime.timedelta(days=1))
        refresh_token = create_refresh_token(identity=str(user.id))

        return make_response(jsonify(access_token=access_token, refresh_token=refresh_token, user=user), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

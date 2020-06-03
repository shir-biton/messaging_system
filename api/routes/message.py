from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId

from models.message import Message
from models.user import User

message_bp = Blueprint('message_bp', __name__)


@message_bp.route("/api/v1/messages", methods=["POST"])
@jwt_required
def write_message():
    data = request.get_json()
    current_user = get_jwt_identity()
    
    try:
        receiver = User.objects.get(id=ObjectId(data.get("receiver")))
        message = Message(sender=current_user, receiver=receiver, subject=data.get("subject"), message=data.get("message"))
        message.save()
        return make_response(jsonify(message), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@message_bp.route("/api/v1/messages", methods=["GET"])
@jwt_required
def get_all_messages():
    current_user = get_jwt_identity()

    try:
        messages = Message.objects(receiver=current_user)
        return make_response(jsonify(messages), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@message_bp.route("/api/v1/messages/unread", methods=["GET"])
@jwt_required
def get_all_unread_messages():
    current_user = get_jwt_identity()

    try:
        messages = Message.objects(receiver=current_user, unread=True)
        return make_response(jsonify(messages), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@message_bp.route("/api/v1/messages/<id>", methods=["GET"])
@jwt_required
def read_message_by_id(id):
    # TODO: Remember to change unread to False
    pass

@message_bp.route("/api/v1/messages/<id>", methods=["DELETE"])
@jwt_required
def delete_message_by_id(id):
    pass
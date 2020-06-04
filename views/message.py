from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.message import Message
from models.user import User
from models.message_box import MessageBox

message_bp = Blueprint('message_bp', __name__)


@message_bp.route("/api/v1/messages", methods=["POST"])
@jwt_required
def write_message():
    data = request.get_json()
    current_user = get_jwt_identity()
    
    try:
        receiver = User.objects.get(email=data.get("receiver"))
        message = Message(sender=current_user, receiver=receiver, subject=data.get("subject"), message=data.get("message"))
        message.save()

        message_box = MessageBox(message_id=message.id, associated_users=([current_user, receiver]))
        message_box.save()

        return make_response(jsonify(message), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@message_bp.route("/api/v1/messages", methods=["GET"])
@jwt_required
def get_all_messages():
    current_user = get_jwt_identity()

    try:
        messages_box = MessageBox.objects(associated_users=current_user)
        messages = [message_box.message_id for message_box in messages_box]
        return make_response(jsonify(messages), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@message_bp.route("/api/v1/messages/unread", methods=["GET"])
@jwt_required
def get_all_unread_messages():
    current_user = get_jwt_identity()

    try:
        messages_box = MessageBox.objects(associated_users=current_user)
        messages = [message_box.message_id for message_box in messages_box if message_box.message_id.unread]
        return make_response(jsonify(messages), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@message_bp.route("/api/v1/messages/<id>", methods=["GET"])
@jwt_required
def read_message_by_id(id):
    current_user = get_jwt_identity()

    try:
        message_box = MessageBox.objects(associated_users=current_user)

        if not message_box:
            return make_response(jsonify({"error": "Bad Request"}), 400)

        message = message_box.first().message_id
        message.update(unread=False)
        message.reload()

        return make_response(jsonify(message), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@message_bp.route("/api/v1/messages/<id>/for_all", methods=["DELETE"])
@jwt_required
def delete_message_for_all(id):
    current_user = get_jwt_identity()

    try:
        messages_box = MessageBox.objects(message_id=id, associated_users=current_user)

        if not messages_box:
            return make_response(jsonify({"error": "Bad Request"}), 400)

        message_box = messages_box.first()
        message = message_box.message_id
        message.delete()
        message_box.delete()

        return make_response(jsonify(message), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@message_bp.route("/api/v1/messages/<id>/for_me", methods=["DELETE"])
@jwt_required
def delete_message_for_me(id):
    current_user = get_jwt_identity()

    try:
        messages_box = MessageBox.objects(message_id=id, associated_users=current_user)

        if not messages_box:
            return make_response(jsonify({"error": "Bad Request"}), 400)
        
        message_box = messages_box.first()
        message_box.update(pull__associated_users=User.objects.get(id=current_user))
        message_box.reload()

        message = message_box.message_id

        if not message_box.associated_users:
            message.delete()
            message_box.delete()

        return make_response(jsonify(message), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
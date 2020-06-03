from flask import Blueprint, jsonify

from models.message import Message

message_bp = Blueprint('message_bp', __name__)


@message_bp.route("/api/v1/messages", methods=["POST"])
@jwt_required
def write_message():
    pass

@message_bp.route("/api/v1/messages", methods=["GET"])
@jwt_required
def get_all_messages():
    pass

@message_bp.route("/api/v1/messages/unread", methods=["GET"])
@jwt_required
def get_all_unread_messages():
    pass

@message_bp.route("/api/v1/messages/<id>", methods=["GET"])
@jwt_required
def get_message_by_id(id):
    pass

@message_bp.route("/api/v1/messages/<id>", methods=["DELETE"])
@jwt_required
def delete_message_by_id(id):
    pass
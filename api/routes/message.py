from flask import Blueprint, jsonify

from models.message import Message

message_bp = Blueprint('message_bp', __name__)
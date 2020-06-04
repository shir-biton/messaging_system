import datetime
from mongoengine import Document, ReferenceField, ListField

from models.user import User
from models.message import Message

class MessageBox(Document):
    message_id = ReferenceField(Message, required=True)
    associated_users = ListField(ReferenceField(User))

    meta = {"collection": "messages_box"}
import datetime
from mongoengine import Document, ReferenceField, ListField

from models.user import User
from models.message import Message

class MessageBox(Document):
    """
    A message box contains a message and its associates users (sender & receiver)
    """
    message_id = ReferenceField(Message, required=True)
    associated_users = ListField(ReferenceField(User))

    meta = {"collection": "messages_box"}
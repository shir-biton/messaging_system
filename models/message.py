import datetime
from mongoengine import Document, StringField, DateTimeField, BooleanField, ReferenceField

from models.user import User

class Message(Document):
    sender = ReferenceField(User, required=True)
    receiver = ReferenceField(User, required=True)
    message = StringField(required=True)
    subject = StringField(max_length=50)
    creation_date = DateTimeField(default=datetime.datetime.utcnow())
    unread = BooleanField(default=True)

    meta = {"collection": "messages"}
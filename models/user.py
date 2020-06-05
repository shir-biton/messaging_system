from mongoengine import Document, StringField, EmailField
from flask_bcrypt import generate_password_hash, check_password_hash

class User(Document):
    name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True, min_length=6)

    meta = {'collection': 'users'}

    def generate_pw_hash(self):
        """
        Generates user's password hash
        """
        self.password = generate_password_hash(password=self.password).decode('utf-8')

    def check_pw_hash(self, password: str) -> bool:
        """
        Comparing user's login password to user collection's password hash
        """
        return check_password_hash(pw_hash=self.password, password=password)

    def save(self, *args, **kwargs):
        # Overwrite Document save method to generate password hash before saving
        self.generate_pw_hash()
        super(User, self).save(*args, **kwargs)
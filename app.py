import os

# flask packages
from flask import Flask, jsonify, make_response
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager

# local packages
from views.user import user_bp
from views.message import message_bp
from config import default_config

def get_flask_app(config: dict = None):
    """
    Initializes Flask app with given configuration.
    :param config: Configuration dictionary
    :return: Flask app
    """
    app = Flask(__name__)
    app.register_blueprint(user_bp)
    app.register_blueprint(message_bp)

    # Configure app
    config = default_config if config is None else config
    app.config.update(config)

    if "MONGODB_URI" in os.environ:
        flask_app.config["MONGODB_SETTINGS"] = {"host": os.environ["MONGODB_URI"], "retryWrites": False}

    if "JWT_SECRET_KEY" in os.environ:
        flask_app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]

    # Init jwt manager
    jwt = JWTManager(app)

    # Init mongoengine
    db = MongoEngine(app)

    return app


if __name__ == "__main__":
    app = get_flask_app()
    app.run(debug=True)

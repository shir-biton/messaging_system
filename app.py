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

    # configure app
    config = default_config if config is None else config
    app.config.update(config)

    jwt = JWTManager(app)
    db = MongoEngine(app)

    return app


if __name__ == "__main__":
    app = get_flask_app()
    app.run(debug=True)

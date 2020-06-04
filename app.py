# flask packages
from flask import Flask, jsonify, make_response
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager

# local packages
from api.routes.user import user_bp
from api.routes.message import message_bp
from models.user import User
from models.message import Message
from config import default_config

def get_flask_app(config: dict = None):
    """
    Initializes Flask app with given configuration.
    :param config: Configuration dictionary
    :return: app
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

app = get_flask_app()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(debug=True)
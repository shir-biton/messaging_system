# flask packages
from flask import Flask, request, jsonify, make_response
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager

# local packages
from api.routes.user import user_bp
from api.routes.message import message_bp
from models.user import User
from models.message import Message

default_config = {
    "JWT_SECRET_KEY": "messaging_app_secret",
    "SECRET_KEY": "dsdsdf",
    "MONGODB_SETTINGS": {
        "db": "messaging_system",
        "host": "localhost",
        "port": 27017
    }
}

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

    return app

app = get_flask_app()
jwt = JWTManager(app)
db = MongoEngine(app)

@app.errorhandler(404)
def not_found(error):
    message = {
        "error":
            {
                "msg": "Not found"
            }
    }

    return make_response(jsonify(message), 404)

@app.route("/")
def hello_world():
    return "Hello World"

if __name__ == "__main__":
    app.run(debug=True)
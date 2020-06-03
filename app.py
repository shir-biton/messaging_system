# flask packages
from flask import Flask, request, jsonify, make_response
from flask_mongoengine import MongoEngine

# local packages
from models.user import User
from models.message import Message

default_config = {
    "SECRET_KEY": "messaging_app_secret",
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

    # configure app
    config = default_config if config is None else config
    app.config.update(config)

    return app

app = get_flask_app()
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

@app.route("/api/v1/users", methods=["POST"])
def new_user():
    return "Hello World"

@app.route("/api/v1/users", methods=["GET"])
def get_users():
    return jsonify(User.objects())

if __name__ == "__main__":
    app.run(debug=True)
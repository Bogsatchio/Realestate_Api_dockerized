import os
from flask import Flask, jsonify
from flask_smorest import Api

from db import db
from resources.general import blp as GeneralBlueprint
from resources.detailed import blp as DetailedBlueprint

def create_app(db_url=None):
    app = Flask(__name__)

    # data for documentation
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "mysql://homestead:secret@mysql/homestead")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    # connect the flask_smorest extension to the flask app
    api = Api(app)

    api.register_blueprint(GeneralBlueprint)
    api.register_blueprint(DetailedBlueprint)

    return app

create_app()


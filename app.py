import os
from flask import Flask, render_template, redirect, url_for, jsonify
from flask_smorest import Api

from flask_bootstrap import Bootstrap5

from db import db
from downloads_form import DownloadsForm
from resources.general import blp as GeneralBlueprint
from resources.detailed import blp as DetailedBlueprint
from local_realestate_scrap.trigger import trigger_dict

def create_app(db_url=None):
    app = Flask(__name__)

    # data for documentation
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Real Estate API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "mysql://homestead:secret@mysql/homestead")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    app.secret_key = "any-string-you-want-just-keep-it-secret"
    bootstrap = Bootstrap5(app)

    # connect the flask_smorest extension to the flask app
    api = Api(app)

    api.register_blueprint(GeneralBlueprint)
    api.register_blueprint(DetailedBlueprint)

# FRONTEND routing
    @app.route("/")
    def home():
        return render_template('index.html')

    @app.route("/downloads", methods=["GET", "POST"])
    def downloads():
        downloads_form = DownloadsForm(db)
        if downloads_form.validate_on_submit():
            out_str = f"/{downloads_form.type_dropdown.data}/{downloads_form.format_dropdown.data}/{downloads_form.city_dropdown.data}/{downloads_form.min_size.data}/{downloads_form.max_size.data}"
            print(out_str)
            return redirect(out_str)
        return render_template('downloads.html', form=downloads_form, values=list(trigger_dict.values()))

    # @app.route("/tables")
    # def tables():
    #     return render_template('tables.html')

    @app.route("/endpoints")
    def endpoints():
        return render_template('endpoints.html')


    return app

create_app()


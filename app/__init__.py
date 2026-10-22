from flask import Flask
from .routes.planet_routes import bp as planet_bp
from .db import db, migrate
from .models.Moon import Moon
import os
from dotenv import load_dotenv

load_dotenv()


def create_app(config=None):
    app = Flask(__name__)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(planet_bp)

    return app

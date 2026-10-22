from flask import Flask
from .routes.planet_routes import bp as planet_bp
from .routes.moon_routes import bp as moon_bp
from .db import db, migrate
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
    app.register_blueprint(moon_bp)

    return app

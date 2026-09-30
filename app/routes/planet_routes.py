from flask import Blueprint
from ..models.Planet import planets


planet_bp = Blueprint("planet_bp", __name__, url_prefix="/planet")


@planet_bp.get("")
def hello_planets():
    return {"message": "Hello form planet"}

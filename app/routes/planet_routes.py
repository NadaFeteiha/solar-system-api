from flask import Blueprint, abort,make_response
from ..models.Planet import planets


planet_bp = Blueprint("planet_bp", __name__, url_prefix="/planet")


@planet_bp.get("")
def hello_planets():
    return {"message": "Hello form planet"}


@planet_bp.get("/all")
def get_all_planets():
    results = []

    for p in planets:
        results.append({"id": p.id, "name": p.name, "description": p.description})

    return results


@planet_bp.get("/<planet_id>")
def get_planet(planet_id):

    planet = validate_planet(planet_id)

    return {"id": planet.id, "name": planet.name, "description": planet.description}


def validate_planet(id):
    try:
        id_planet = int(id)
    except ValueError:
        response = {"message": f"Invalid planet id: {id}"}
        abort(make_response(response, 400))

    for p in planets:
        if p.id == id_planet:
            return p

    response = {"message": f"Planet not found: {id}"}
    abort(make_response(response, 404))

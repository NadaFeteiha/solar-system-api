from flask import Blueprint, abort, make_response, request
from ..models.Planet import Planet
from ..db import db


planet_bp = Blueprint("planet_bp", __name__, url_prefix="/planet")


@planet_bp.get("")
def hello_planets():
    return {"message": "Hello form planet"}


@planet_bp.post("")
def add_planets():
    request_body = request.get_json()

    name = request_body["name"]
    description = request_body["description"]
    num_moons = int(request_body["num_moons"])

    new_planet = Planet(name=name, description=description, number_of_moons=num_moons)
    db.session.add(new_planet)
    db.session.commit()

    response = {
        "id": new_planet.id,
        "name": new_planet.name,
        "description": new_planet.description,
        "num_moons": new_planet.number_of_moons,
    }

    return response, 201


@planet_bp.get("/all")
def get_all_planets():
    results = []
    query = db.select(Planet)
    planets = db.session.scalars(query)

    for p in planets:
        results.append({"id": p.id, "name": p.name,"number_of_moons": p.number_of_moons ,"description": p.description})

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

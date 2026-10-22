from flask import Blueprint, abort, make_response, request, Response
from ..models.Planet import Planet
from ..models.Moon import Moon
from ..db import db
from .route_utilities import validate_model, validate_int_param, validate_request_body

bp = Blueprint("planet_bp", __name__, url_prefix="/planets")


@bp.post("")
def create_planet():
    request_body = request.get_json()
    new_planet = validate_request_body(Planet, request_body)

    db.session.add(new_planet)
    db.session.commit()
    return new_planet.to_dict(), 201


@bp.get("")
def get_all_planets():
    query = db.select(Planet)

    name_param = request.args.get("name")
    if name_param:
        query = query.where(Planet.name.ilike(f"%{name_param}%"))

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Planet.description.ilike(f"%{description_param}%"))

    min_moons_param = request.args.get("min_moons")
    if min_moons_param:
        min_moons = validate_int_param("min_moons", min_moons_param)
        query = query.where(Planet.number_of_moons >= min_moons)

    max_moons_param = request.args.get("max_moons")
    if max_moons_param:
        max_moons = validate_int_param("max_moons", max_moons_param)
        query = query.where(Planet.number_of_moons <= max_moons)

    sort_param = request.args.get("sort")
    if sort_param == "name":
        sort_column = Planet.name
    elif sort_param == "num_moons":
        sort_column = Planet.number_of_moons
    else:
        sort_column = Planet.id

    order_param = request.args.get("order")
    if order_param == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    planets = db.session.scalars(query)

    response = []
    for planet in planets:
        response.append(planet.to_dict())

    return response, 200


@bp.get("/<planet_id>")
def get_one_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    return planet.to_dict(), 200


@bp.put("/<planet_id>")
def update_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    request_body = request.get_json()

    if "name" in request_body:
        planet.name = request_body["name"]

    if "description" in request_body:
        planet.description = request_body["description"]

    if "num_moons" in request_body:
        try:
            planet.number_of_moons = int(request_body["num_moons"])
        except ValueError:
            abort(
                make_response(
                    {"message": "Invalid request: num_moons must be an integer"}, 400
                )
            )

    db.session.commit()

    return planet.to_dict(), 200


@bp.delete("/<planet_id>")
def delete_planet(planet_id):
    planet = validate_model(Planet, planet_id)

    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.post("/<planet_id>/moons")
def create_moon_with_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    request_body = request.get_json()
    new_moon = validate_request_body(Moon, request_body)
    new_moon.planet = planet

    db.session.add(new_moon)
    db.session.commit()
    return new_moon.to_dict(), 201


@bp.get("/<planet_id>/moons")
def get_moons_by_planet(planet_id):
    planet = validate_model(Planet, planet_id)

    response = []
    for moon in planet.moons:
        response.append(moon.to_dict())

    return response, 200

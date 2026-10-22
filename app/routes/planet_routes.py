from flask import Blueprint, abort, make_response, request, Response
from ..models.Planet import Planet
from ..models.Moon import Moon
from ..db import db
from .route_utilities import (
    validate_model,
    validate_int_param,
    create_model_with_response,
    get_models_with_filters,
    update_model_with_response,
)

bp = Blueprint("planet_bp", __name__, url_prefix="/planets")


@bp.post("")
def create_planet():
    request_body = request.get_json()
    return create_model_with_response(Planet, request_body)


@bp.get("")
def get_all_planets():
    filters = dict(request.args)
    query = db.select(Planet)

    min_moons_param = filters.pop("min_moons", None)
    if min_moons_param:
        min_moons = validate_int_param("min_moons", min_moons_param)
        query = query.where(Planet.number_of_moons >= min_moons)

    max_moons_param = filters.pop("max_moons", None)
    if max_moons_param:
        max_moons = validate_int_param("max_moons", max_moons_param)
        query = query.where(Planet.number_of_moons <= max_moons)

    if filters.get("sort") == "num_moons":
        filters["sort"] = "number_of_moons"

    return get_models_with_filters(Planet, filters, query), 200


@bp.get("/<planet_id>")
def get_one_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    return planet.to_dict(), 200


@bp.put("/<planet_id>")
def update_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    request_body = dict(request.get_json())

    if "num_moons" in request_body:
        request_body["number_of_moons"] = validate_int_param(
            "num_moons", request_body.pop("num_moons")
        )

    return update_model_with_response(planet, request_body)


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
    request_body["planet_id"] = planet.id
    return create_model_with_response(Moon, request_body)


@bp.get("/<planet_id>/moons")
def get_moons_by_planet(planet_id):
    planet = validate_model(Planet, planet_id)

    response = []
    for moon in planet.moons:
        response.append(moon.to_dict())

    return response, 200


@bp.delete("/<planet_id>/moons/<moon_id>")
def remove_moon_from_planet(planet_id, moon_id):
    planet = validate_model(Planet, planet_id)
    moon = validate_model(Moon, moon_id)

    if moon.planet_id != planet.id:
        abort(
            make_response(
                {"message": f"Moon {moon_id} does not belong to Planet {planet_id}"},
                404,
            )
        )

    moon.planet = None
    db.session.commit()

    return Response(status=204, mimetype="application/json")

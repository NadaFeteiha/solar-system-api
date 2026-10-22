from flask import Blueprint, abort, make_response, request, Response
from ..models.Moon import Moon
from ..models.Planet import Planet
from ..db import db
from .route_utilities import (
    validate_model,
    get_models_with_filters,
    create_model_with_response,
    update_model_with_response,
)

bp = Blueprint("moon_bp", __name__, url_prefix="/moons")


@bp.post("")
def create_moon():
    request_body = request.get_json()

    if request_body.get("planet_id") is not None:
        validate_model(Planet, request_body["planet_id"])
    
    return create_model_with_response(Moon, request_body)


@bp.get("")
def get_all_moons():
    return get_models_with_filters(Moon, request.args)


@bp.get("/<moon_id>")
def get_one_moon(moon_id):
    moon = validate_model(Moon, moon_id)
    return moon.to_dict()


@bp.put("/<moon_id>")
def update_moon(moon_id):
    moon = validate_model(Moon, moon_id)
    request_body = request.get_json()

    if "planet_id" in request_body:
        validate_model(Planet, request_body["planet_id"])

    return update_model_with_response(moon, request_body)


@bp.delete("/<moon_id>")
def delete_moon(moon_id):
    moon = validate_model(Moon, moon_id)
    db.session.delete(moon)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.get("/<moon_id>/planet")
def get_planet_of_moon(moon_id):
    moon = validate_model(Moon, moon_id)

    if not moon.planet:
        abort(make_response({"message": f"Moon {moon_id} has no planet"}, 404))

    return moon.planet.to_dict(), 200

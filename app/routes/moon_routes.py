from flask import Blueprint, request, Response
from ..models.Moon import Moon
from ..db import db
from .route_utilities import (
    validate_model,
    validate_request_body,
    get_models_with_filters,
    create_model_with_response,
)

bp = Blueprint("moon_bp", __name__, url_prefix="/moons")


@bp.post("")
def create_moon():
    request_body = request.get_json()
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
    updated_moon = validate_request_body(Moon, request_body)

    moon.size = updated_moon.size
    moon.description = updated_moon.description

    db.session.commit()

    return Response(status=204, mimetype="application/json")  # 204 No Content


@bp.delete("/<moon_id>")
def delete_moon(moon_id):
    moon = validate_model(Moon, moon_id)
    db.session.delete(moon)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

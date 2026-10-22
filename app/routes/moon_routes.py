from flask import Blueprint, abort, make_response, request, Response
from ..models.Moon import Moon
from ..db import db
from .route_utilities import validate_model, validate_int_param, validate_request_body

bp = Blueprint("moon_bp", __name__, url_prefix="/moons")


@bp.post("")
def create_moon():
    request_body = request.get_json()
    new_moon = validate_request_body(Moon, request_body)

    db.session.add(new_moon)
    db.session.commit()
    return new_moon.to_dict(), 201


@bp.get("")
def get_all_moons():
    query = db.select(Moon)

    size_param = request.args.get("size")
    if size_param:
        query = query.where(Moon.size.ilike(f"%{size_param}%"))

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Moon.description.ilike(f"%{description_param}%"))

    sort_param = request.args.get("sort")
    if sort_param == "size":
        sort_column = Moon.size
    else:
        sort_column = Moon.id

    order_param = request.args.get("order")
    if order_param == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    moons = db.session.scalars(query)

    response = []
    for moon in moons:
        response.append(moon.to_dict())

    return make_response(response, 200)

from flask import Blueprint, abort, make_response, request, Response
from ..models.Planet import Planet
from ..db import db

planet_bp = Blueprint("planet_bp", __name__, url_prefix="/planets")


@planet_bp.post("")
def create_planet():
    request_body = request.get_json()
    new_planet = validate_request_body(request_body)

    db.session.add(new_planet)
    db.session.commit()
    return new_planet.to_dict(), 201


@planet_bp.get("")
def get_all_planets():

    response = []
    query = db.select(Planet)

    name_param = request.args.get("name")
    if name_param:
        query = query.where(Planet.name.ilike(f"%{name_param}%"))
    
    description_param = request.args.get("description")
    if description_param:
        query = query.where(Planet.description.ilike(f"%{description_param}%"))

    moons_param = request.args.get("num_moons")
    if moons_param:
        query = query.where(Planet.number_of_moons == moons_param)
    
    query = query.order_by(Planet.id)
    planets = db.session.scalars(query)

    for planet in planets:
        response.append(planet.to_dict())

    return response, 200


@planet_bp.get("/<planet_id>")
def get_one_planet(planet_id):
    planet = validate_planet(planet_id)
    return planet.to_dict(), 200


@planet_bp.put("/<planet_id>")
def update_planet(planet_id):
    planet = validate_planet(planet_id)
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

    return planet.to_dict()


@planet_bp.delete("/<planet_id>")
def delete_planet(planet_id):
    planet = validate_planet(planet_id)

    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


# ==========================================
#            helper functions
# ==========================================
def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        abort(make_response({"message": f"Planet id {planet_id} invalid"}, 400))

    planet = db.session.get(Planet, planet_id)

    if not planet:
        abort(make_response({"message": f"Planet {planet_id} not found"}, 404))

    return planet


def validate_request_body(request_body):
    try:
        if (
            "name" not in request_body
            or "description" not in request_body
            or "num_moons" not in request_body
        ):
            abort(
                make_response(
                    {
                        "message": "Invalid data should have name, description, num_moons"
                    },
                    400,
                )
            )

        new_planet = Planet(
            name=request_body["name"],
            description=request_body["description"],
            number_of_moons=int(request_body["num_moons"]),
        )

    except ValueError:
        abort(
            make_response(
                {"message": "Invalid request: num_moons must be an integer"}, 400
            )
        )
    return new_planet

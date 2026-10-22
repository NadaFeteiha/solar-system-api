from flask import abort, make_response
from ..db import db


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        abort(make_response({"message": f"{cls.__name__} id {model_id} invalid"}, 400))

    model = db.session.get(cls, model_id)

    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))

    return model


def validate_int_param(param_name, value):
    try:
        return int(value)
    except ValueError:
        abort(
            make_response(
                {"message": f"Invalid request: {param_name} must be an integer"}, 400
            )
        )


def validate_request_body(cls, request_body):
    try:
        new_model = cls.from_dict(request_body)
    except KeyError as error:
        abort(
            make_response({"message": f"Invalid request: missing {error.args[0]}"}, 400)
        )
    except ValueError as error:
        abort(make_response({"message": f"Invalid request: {error}"}, 400))

    return new_model


def get_models_with_filters(cls, filters):
    query = db.session.query(cls)

    for key, value in filters.items():
        if hasattr(cls, key):
            column = getattr(cls, key)
            query = query.filter(column == value)
        else:
            abort(
                make_response(
                    {"message": f"Invalid filter: {key} is not a valid attribute"}, 400
                )
            )

    models = query.all()
    model_dicts = []
    for model in models:
        model_dicts.append(model.to_dict())

    return model_dicts


def create_model_with_response(cls, request_body):
    new_model = validate_request_body(cls, request_body)

    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201
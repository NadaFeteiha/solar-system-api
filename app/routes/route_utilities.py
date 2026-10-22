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


def get_column(cls, attribute):
    invalid_response = make_response(
        {"message": f"Invalid attribute: {attribute}"}, 400
    )

    if not hasattr(cls, attribute):
        abort(invalid_response)

    column = getattr(cls, attribute)

    if not hasattr(column, "type"):
        abort(invalid_response)

    return column


def get_models_with_filters(cls, filters, query=None):
    if query is None:
        query = db.select(cls)

    sort_column = cls.id
    order = "asc"

    for key, value in filters.items():
        if key == "sort":
            sort_column = get_column(cls, value)
        elif key == "order":
            order = value
        else:
            column = get_column(cls, key)
            if column.type.python_type is str:
                query = query.where(column.ilike(f"%{value}%"))
            else:
                query = query.where(column == validate_int_param(key, value))

    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    models = db.session.scalars(query)
    model_dicts = []
    for model in models:
        model_dicts.append(model.to_dict())

    return model_dicts


def update_model_with_response(model, request_body):
    cls = type(model)

    for key, value in request_body.items():
        if key == "id":
            abort(
                make_response({"message": "Invalid request: id cannot be updated"}, 400)
            )

        column = get_column(cls, key)
        if column.type.python_type is int and value is not None:
            value = validate_int_param(key, value)

        setattr(model, key, value)

    db.session.commit()

    return model.to_dict(), 200


def create_model_with_response(cls, request_body):
    new_model = validate_request_body(cls, request_body)

    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201

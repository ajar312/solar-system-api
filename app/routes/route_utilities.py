from flask import abort, make_response 
from ..db import db

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response = {"message": f"planet {model_id} invalid"}
        abort(make_response(response , 400))

    query = db.select(cls).where(Planet.id == model_id)
    model = db.session.scalar(query)

    if not model:

        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))
    return model
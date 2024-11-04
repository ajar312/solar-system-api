from flask import Blueprint, abort, make_response, request, Response
from app.models.planet import Planet
from ..db import db
from .route_utilities import validate_model

planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

@planets_bp.post("")
def create_planet():
    request_body = request.get_json()
    try:
        new_planet = Planet.from_dict(request_body) 
    except KeyError as e:
        response = {"message": f"Invalid request: missing {e.args[0]}"}
        abort(make_response(response, 400))
        
        db.session.add(new_planet)
        db.session.commit()
        
        response = new_planet.to_dict()
        return response, 201
    

@planets_bp.get("")
def get_all_planets():
    # description_param = request.args.get("description")
    # color_param = request.args.get("color")

    # query = db.select(Planet)
    # if description_param:
    #     query = query.where(Planet.description == description_param)

    query = db.select(Planet)

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Planet.title.ilike(f"%{description_param}%"))

    color_param = request.args.get("color")
    if color_param:
        query = query.where(Planet.color.ilike(f"%{color_param}%"))
    planets = db.session.scalars(query.order_by(Planet.id))  
    
    planets_response = []
    for planet in planets:
        planets_response.append(
            {
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "color": planet.color,
            }
        )

    return planets_response

@planets_bp.get("/<planet_id>")
def get_one_planet(planet_id):
    planet = validate_model(planet_id)
    
    return {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "color": planet.color,
    }


@planets_bp.put("/<planet_id>")
def update_planet(planet_id):
    planet = validate_model(planet_id)
    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.color = request_body["color"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@planets_bp.delete("/<planet_id>")
def delete_planet(planet_id):
    planet = validate_model(planet_id)
    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

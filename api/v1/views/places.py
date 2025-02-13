#!/usr/bin/python3
# Author: Joana Casallas
"""Place view"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity


@app_views.route("cities/<string:city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieve all places by its city_id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    list_places = [place.to_dict() for place in city.places]
    return jsonify(list_places)


@app_views.route("/places/<string:place_id>", methods=["GET"],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieve an place by its ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<string:place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete a place by its ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("cities/<string:city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """Create place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    if 'name' not in data:
        abort(400, description="Missing name")
    user_id = storage.get(User, data['user_id'])
    if user_id is None:
        abort(404)
    new_place = Place(**data)
    new_place.city_id = city_id
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places_search", methods=["POST"],
                 strict_slashes=False)
def all_places_id():
    """Return list of places according the filter required"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if data is None:
        return [place.to_dict() for place in storage.all(Place).values()]
    list_ids = []
    list_cities = []
    list_places = []
    for requirement in data:
        for id_obj in data[requirement]:
            list_ids.append(id_obj)
        if requirement == "states":
            all_states = storage.all(State)
            for k, v in all_states.items():
                if v.id in list_ids:
                    for city in v.cities:
                        list_cities.append(city)
        elif requirement == "cities":
            all_cities = storage.all(City)
            for k, v in all_cities.items():
                if v.id in list_ids:
                    list_cities.append(v)
        elif requirement == "amenities":
            all_places = storage.all(Place)
            for place in all_places.items():
                for k, v in place.amenities:
                    if v.id in list_ids:
                        list_places.append(v.to_dict())
    for city in list_cities:
        for place in city.places:
            if place not in list_places:
                list_places.append(place.to_dict())
    return jsonify(list_places), 201


@app_views.route("/places/<string:place_id>", methods=["PUT"],
                 strict_slashes=False)
def update_place(place_id):
    """Update place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, description="Place not found")
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    for k, v in data.items():
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, k, v)
    storage.save()
    return jsonify(place.to_dict()), 200

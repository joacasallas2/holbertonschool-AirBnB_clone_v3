#!/usr/bin/python3
# Author: Joana Casallas
"""Amenities sview"""
from flask import jsonify, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route("places/<string:place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def get_amenities(place_id):
    """Retrieve all amenities by the place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    list_amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(list_amenities)


@app_views.route("places/<string:place_id>/amenities/<string:amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """Delete a amenity by its ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("places/<string:place_id>/amenities/<string:amenity_id>",
                 methods=["POST"],
                 strict_slashes=False)
def link_amenity_place(place_id, amenity_id):
    """Link an amenity to a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201

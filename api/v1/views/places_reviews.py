#!/usr/bin/python3
# Author: Joana Casallas
"""Reviewsview"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review


@app_views.route("places/<string:place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_reviews(place_id):
    """Retrieve all reviews by the place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    list_reviews = [review.to_dict() for review in place.reviews]
    return jsonify(list_reviews)


@app_views.route("/reviews/<string:review_id>", methods=["GET"],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieve a review by its ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<string:review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete a review by its ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("places/<string:place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """Create review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if "user_id" not in data:
        abort(400, description="Missing user_id")
    if "text" not in data:
        abort(400, description="Missing text")
    user_id = storage.get(Place, data['user_id'])
    if user_id is None:
        abort(404)
    new_review = Review(**data)
    new_review.place_id = place_id
    new_review.user_id = user_id
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<string:review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """Update review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404, description="Review not found")
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    for k, v in data.items():
        if k not in ['id', 'place_id', 'user_id', 'created_at', 'updated_at']:
            setattr(review, k, v)
    storage.save()
    return jsonify(review.to_dict()), 200

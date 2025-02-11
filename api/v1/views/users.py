#!/usr/bin/python3
# Author: Joana Casallas
"""User view"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"],
                 strict_slashes=False)
def get_users():
    """Retrieve all users"""
    list_users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(list_users)


@app_views.route("/users/<string:user_id>", methods=["GET"],
                 strict_slashes=False)
def get_user(user_id):
    """Retrieve an user by its ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<string:user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """Delete a user by its ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"],
                 strict_slashes=False)
def create_user():
    """Create user"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    if 'email' not in data:
        abort(400, description="Missing email")
    if 'password' not in data:
        abort(400, description="Missing password")
    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<string:user_id>", methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """Update user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404, description="User not found")
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    for k, v in data.items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, k, v)
    storage.save()
    return jsonify(user.to_dict()), 200

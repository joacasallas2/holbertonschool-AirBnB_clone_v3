#!/usr/bin/python3
# Author: Joana Casallas
"""States view"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """Retrieve all states"""
    list_states = [v.to_dict() for v in (storage.all(State).values())]
    return jsonify(list_states)


@app_views.route("/states/<string:state_id>", methods=["GET"],
                 strict_slashes=False)
def get_state(state_id):
    """Retrieve a state by its ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<string:state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete a state by its ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/", methods=["POST"],
                 strict_slashes=False)
def create_state():
    """Create state"""
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<string:state_id>", methods=["PUT"],
                 strict_slashes=False)
def update_state(state_id):
    """Update state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, v)
    storage.save()
    return jsonify(state.to_dict()), 200

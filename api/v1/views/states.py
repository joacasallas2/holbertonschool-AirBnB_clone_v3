#!/usr/bin/python3
# Author: Joana Casallas
"""States view"""
from flask import jsonify, abort, request, make_response
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
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route("/states/<string:state_id>", methods=["PUT"],
                 strict_slashes=False)
def update_state(state_id):
    """Update state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, v)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)

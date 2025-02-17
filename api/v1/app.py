#!/usr/bin/python3
# Author: Joana Casallas
"""Flask App"""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://0.0.0.0"}})


swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "HBNB API",
        "description": "RESTFul API for HBNB",
        "version": "1.0.0",
        "contact": {
            "email": "joacasallas@gmail.com"
        }
    },
    "host": "127.0.0.1:5000",
    "basePath": "/api/v1",
    "schemes": ["http"],
    "definitions": {  # <- Added missing comma here
        "Place": {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "user_id": {"type": "string"},
                "city_id": {"type": "string"},
                "name": {"type": "string"},
                "description": {"type": "string"},
                "number_rooms": {"type": "integer"},
                "number_bathrooms": {"type": "integer"},
                "price_by_night": {"type": "integer"}
            }
        }
    }
})

app.register_blueprint(app_views)


@app.errorhandler(404)
def page_not_found(e):
    """handler error 404"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown_db(exception):
    """Remove the current SQLAlchemy session after each request"""
    storage.close()


if __name__ == '__main__':
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", "5000"))
    app.run(host=host, port=port, threaded=True)

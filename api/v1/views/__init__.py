#!/usr/bin/python3
# Author: Joana Casallas
"""Blueprint app_views"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.index import *  # noqa: F401
from api.v1.views.states import *  # noqa: F401
from api.v1.views.cities import *  # noqa: F401
from api.v1.views.amenities import *  # noqa: F401
from api.v1.views.users import *  # noqa: F401
from api.v1.views.places import *  # noqa: F401
from api.v1.views.places_reviews import *  # noqa: F401
from api.v1.views.places_amenities import *  # noqa: F401

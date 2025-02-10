#!/usr/bin/python3
# Author: Joana Casallas
"""Blueprint app_views"""
from flask import Blueprint, render_template, abort


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.index import *  # noqa: F401
from api.v1.views.states import *  # noqa: F401

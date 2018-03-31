__author__ = 'Cedric Da Costa Faro'

from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.auth import routes
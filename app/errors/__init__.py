__author__ = 'Cedric Da Costa Faro'

from flask import Blueprint

bp = Blueprint('errors', __name__)

from app.errors import handlers
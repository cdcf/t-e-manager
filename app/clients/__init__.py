__author__ = 'Cedric Da Costa Faro'

from flask import Blueprint

bp = Blueprint('clients', __name__)

from app.clients import routes
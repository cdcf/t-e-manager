__author__ = 'Cedric Da Costa Faro'

from flask import Blueprint

bp = Blueprint('currencies', __name__)

from app.currencies import routes
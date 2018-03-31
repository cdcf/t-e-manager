__author__ = 'Cedric Da Costa Faro'

from flask import Blueprint

bp = Blueprint('expenses', __name__)

from app.expenses import routes

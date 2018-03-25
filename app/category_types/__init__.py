__author__ = 'Cedric Da Costa Faro'

from flask import Blueprint

bp = Blueprint('category_types', __name__)

from app.category_types import routes
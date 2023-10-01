from flask_smorest import Blueprint

bp = Blueprint('therapists', __name__, description='Ops on Therapists')

from . import routes
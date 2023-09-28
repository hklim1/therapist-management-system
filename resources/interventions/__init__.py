from flask_smorest import Blueprint

bp = Blueprint('interventions', __name__, url_prefix='/intervention')

from . import routes
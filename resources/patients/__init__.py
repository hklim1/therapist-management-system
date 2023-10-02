from flask_smorest import Blueprint

bp = Blueprint('patients', __name__, description='Ops on Patients')

from . import routes
from . import auth_routes
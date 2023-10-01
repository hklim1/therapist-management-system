from flask import Flask
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from Config import Config
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

from resources.patients import bp as patient_bp
api.register_blueprint(patient_bp)
from resources.interventions import bp as intervention_bp
api.register_blueprint(intervention_bp)
from resources.therapists import bp as therapist_bp
api.register_blueprint(therapist_bp)

from resources.patients import routes
from resources.interventions import routes
from resources.therapists import routes

from resources.patients.PatientModel import PatientModel
# you must make sure to put this line before "db =" to avoid a circular import error
from resources.interventions.InterventionModel import InterventionModel
from resources.therapists.TherapistModel import TherapistModel

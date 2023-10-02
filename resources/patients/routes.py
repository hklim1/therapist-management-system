from flask.views import MethodView
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from schemas import InterventionSchema, UpdatePatientSchema, PatientSchema, AuthPatientSchema, PatientSchemaNested
from . import bp
from .PatientModel import PatientModel
from ..therapists.TherapistModel import TherapistModel
from flask_jwt_extended import jwt_required, get_jwt_identity

from db import patients, interventions

@bp.route('/patient')
class PatientList(MethodView):
    
# def get_patients():
#     return {'patients': patients}, 200
    @bp.response(200, PatientSchema(many = True))
    def get(self):
        patients = PatientModel.query.all()
        # the query above is running a query in our real database to get ALL the patients.
        return patients
    
    # @app.post('/patient')
    # def add_patient():
    #     patient_data = request.get_json()
    #     patients[uuid4().hex] = patient_data
    #     return patient_data, 201
    
    # WE MOVED THIS TO TO AUTH_ROUTES
    # @bp.arguments(PatientSchema)
    # @bp.response(201, PatientSchema)
    # def post(self, patient_data):
    #     patient = PatientModel()
    #     try:
    #         patient.from_dict(patient_data)
    #         patient.save()
    #         return patient_data
    #     except IntegrityError:
    #         abort(400, message='Patient is already in medical record system.')

# @app.delete('/patient/<patient_id>')
# def discharge_patient(patient_id):
#     try:
#         store = patients[patient_id]['name']
#         del patients[patient_id]
#     except KeyError:
#         return {'message': 'patient not found'}, 400
#     return {'message':f"{store} has been discharged and deleted from database"}, 202
# ************************************************************************************
    @jwt_required()
    @bp.arguments(AuthPatientSchema)
    def delete(self, patient_data):
        patient_id = get_jwt_identity()
        patient = PatientModel.query.get(patient_id)
        # .first() gives us the first value. you can also give .all() which would return a list, but because there is only 1 unique username or user_id, you would have to then index into the list which is just extra step.
        if patient and patient.first_name == patient_data['first_name'] and patient.last_name == patient_data['last_name'] and patient.id == patient_data['id']:
            patient.delete()
            return {'message':f'{patient_data["first_name"]} {patient_data["last_name"]} has been discharged and removed from medical record system'}, 202
        abort(400, message='Patient ID Invalid')

    @jwt_required()
    @bp.arguments(UpdatePatientSchema)
    @bp.response(202, PatientSchema)
    def put(self, patient_data):
        patient_id = get_jwt_identity()
        patient = PatientModel.query.get_or_404(patient_id, description="Patient Not Found")
        if patient:
            try:
                patient.from_dict(patient_data)
                patient.save()
                return patient
            except IntegrityError:
                abort(400, message='Patient already exists in system.')

@bp.route('/patient/<patient_id>')
class Patient(MethodView):

    # @bp.response(200, PatientSchemaNested)
    # def get(self, patient_id):
    #     patient = PatientModel.query.get_or_404(patient_id, description='Patient Not Found')
    #     return patient

    @bp.response(200, PatientSchemaNested)
    def get(self, patient_id):
        patient = None
        if patient_id.isdigit():
            patient = PatientModel.query.get(patient_id)
        if not patient:
            patient = PatientModel.query.filter_by(last_name=patient_id).first() #I know that this is not secure at all but it is the only thing I could think of to test out this new function since I didn't make this with usernames!!
        if patient:
            return patient
        abort(400, message="Please enter valid ID or last name")


# @app.get('/patient/<patient_id>')
# def get_patient(patient_id):
#     try:
#         patient = patients[patient_id]
#         return patient, 200
#     except KeyError:
#         return {'message':'patient not found'}, 400

# @app.put('/patient/<patient_id>')
# def update_patient(patient_id):
#     patient_data = request.get_json()
#     try:
#         patient = patients[patient_id]
#         patient['recovery week'] = patient_data['new recovery week']
#         return patient, 200
#     except KeyError:
#         return {'message': 'patient not found'}, 400

# This became redundant after we made PatientSchemaNested
# @bp.get('/patient/<patient_id>/intervention')
# @bp.response(200, InterventionSchema(many=True))
# def get_patient_interventions(patient_id):
#   if patient_id not in patients:
#     abort(404, message='Patient not found')
#   patient_interventions = [intervention for intervention in interventions.values() if intervention['patient_id'] == patient_id]
#   return patient_interventions, 200

# @app.get('/patient/<patient_id>/interventions')
# def get_patient_interventions(patient_id):
#     if patient_id not in patients:
#         return {'message': 'patient not found'}, 400
#     return interventions[patient_id], 200
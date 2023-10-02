from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token

from schemas import PatientSchema, AuthPatientSchema

from . import bp
from .PatientModel import PatientModel
# ===========QUESTION: Re-explain why we don't use MethodView for our endpoints? d4AM 1:20

# @bp.route ONLY ALLOWS A GET REQUEST by default. must write bp.route(methods=['POST']) to change
@bp.post('/register') #This is one of our endpoints, we are creating a pt therefore are POSTING a pt
@bp.arguments(PatientSchema)
@bp.response(201, PatientSchema)
def register(patient_data):
    patient = PatientModel()
    patient.from_dict(patient_data)
    duplicate = PatientModel.query.filter_by(last_name=patient_data['last_name'], first_name=patient_data['first_name'], doi_dos=patient_data['doi_dos']).first()
    if duplicate:
        abort(400, message='Patient already registered')
    try:
        patient.save()
        return patient_data
    except IntegrityError:
        abort(400, message='Patient already registered')

# EXAMPLE OF USING METHODVIEW:
# class RegisterUser(MethodView): #NOTICE THIS DIFF
#     @bp.arguments(PatientSchema)
#     @bp.response(201, PatientSchema)
#     def post(self, patient_data): # AND THIS DIFF
#     patient = PatientModel()
#     patient.from_dict(self, patient_data) # NEED TO ADD SELF
#     try:
#         patient.save()
#         return patient_data
#     except IntegrityError:
#         abort(400, message='Patient already registered')

@bp.post('/login') # User is sending us info, therefore it is POST request
@bp.arguments(AuthPatientSchema)
def login(login_info):
    if 'id' not in login_info or 'first_name' not in login_info or 'last_name' not in login_info:
        abort(400, message='Please include Patient ID#, First Name, and Last Name!')
#   if 'username' in login_info: #You could put this here IF you wanted them to have option to login with EITHER username OR email.
#     user = UserModel.query.filter_by(username=login_info['username']).first()
#   else:
#     user = UserModel.query.filter_by(email=login_info['email']).first()
    if 'id' in login_info and 'first_name' in login_info:
        patient = PatientModel.query.filter_by(id=login_info['id'], first_name=login_info['first_name'], last_name=login_info['last_name']).first()
    if patient:
        access_token = create_access_token(identity=patient.id)
        return {'access_token':access_token}
    abort(400, message='Invalid Patient ID#, First Name, or Last Name')

# @bp.route('/logout')
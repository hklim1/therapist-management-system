from flask import request
from uuid import uuid4
from flask.views import MethodView
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity

from resources.patients.PatientModel import PatientModel

from .InterventionModel import InterventionModel
from schemas import InterventionSchema, UpdateInterventionSchema
from . import bp


@bp.route('/')
class InterventionList(MethodView):

# TO UTILIZE AN ACCESS TOKEN, MAKE A NEW HEADER ON YOUR GET/POST/PUT/DELETE REQUEST IN INSOMNIA (OR WHEREVER) CALLED "AUTHORIZATION". IN DESCRIPTION WRITE "Bearer <access_token>" NO <>
    @jwt_required()
    @bp.response(200, InterventionSchema(many=True))
    # need to add this bp.response to serialize the data, which will prevent code breaking
    def get(self):
        return InterventionModel.query.all()
# @app.get('/intervention')
# def get_interventions():
#     return {'interventions': interventions}, 200

    @jwt_required()
    @bp.arguments(InterventionSchema)
    @bp.response(200, InterventionSchema)
    def post(self, intervention_data):
        patient_id = get_jwt_identity()
        i = InterventionModel(**intervention_data, patient_id=patient_id)
        try:
            i.save()
            return i
        except IntegrityError:
            abort(400, message="Invalid Patient ID")
# **intervention_data == modalities = intervention_data['modalities'], arom = intervention_data['arom'], etc. ** destructures the dict and spreading it out. It's saying give me key(modalities) and its value(whatever is in there).

# @app.post('/intervention')
# def create_intervention():
#     intervention_data = request.get_json()
#     interventions[uuid4().hex] = intervention_data
#     return intervention_data, 201

@bp.route('/<intervention_id>')
class Intervention(MethodView):

    @jwt_required()
    @bp.response(200, InterventionSchema) #this is a flask-smorest decorator
    def get(self, intervention_id):
        i = InterventionModel.query.get(intervention_id)
        if i:
            return i
        abort(400, 'Invalid Intervention ID')
      # return {'message': 'post not found'}, 400
# @app.get('/intervention/<intervention_id>')
# def get_intervention(intervention_id):
#     try:
#         intervention = interventions[intervention_id]
#         return intervention, 200
#     except KeyError:
#         return {'message': 'intervention not found'}, 400

    @jwt_required()
    @bp.arguments(UpdateInterventionSchema)
    @bp.response(200, UpdateInterventionSchema)
    def put(self, intervention_data, intervention_id):
        i = InterventionModel.query.get(intervention_id)
        if i and intervention_data != {}:
            patient_id = get_jwt_identity()
            if i.patient_id == patient_id:
                if 'modalities' in intervention_data:
                    i.modalities = intervention_data['modalities']
                if 'AROM' in intervention_data:
                    i.AROM = intervention_data['AROM']
                if 'PROM' in intervention_data:
                    i.PROM = intervention_data['PROM']
                if 'strengthening' in intervention_data:
                    i.strengthening = intervention_data['strengthening']
                i.save()
                return i
            else:
                abort(401, message='Unauthorized')
        abort(400, message="Invalid Intervention Data")
# what if they send us an empty value?
                
                
        # if intervention_id in interventions:
        #     intervention = interventions[intervention_id]
        #     if intervention_data['intervention_id'] != intervention['intervention_id']:
        #         abort(400, message="Cannot edit other patient's intervention")
        #     intervention['modalities'] = intervention_data['modalities']
        #     intervention['AROM'] = intervention_data['AROM']
        #     intervention['PROM'] = intervention_data['PROM']
        #     intervention['strengthening'] = intervention_data['strengthening']
        #     return intervention, 200
        # abort(404, message='Intervention not Found')
# @app.put('/intervention/<intervention_id>')
# def edit_post(intervention_id):
#     intervention_data = request.get_json()
#     if intervention_id in interventions:
#         intervention = interventions[intervention_id]
#         intervention['modalities'] = intervention_data['modalities']
#         intervention['AROM'] = intervention_data['AROM']
#         intervention['PROM'] = intervention_data['PROM']
#         intervention['strengthening'] = intervention_data['strengthening']
#         return intervention, 200
#     return {'message': 'Intervention not found'}, 400
    @jwt_required()
    def delete(self, intervention_id):
        patient_id = get_jwt_identity()
        i = InterventionModel.query.get(intervention_id)
        if i:
            if i.patient_id == patient_id:
                i.delete()
                return {'message': f'Intervention for Patient #{patient_id} deleted'}, 202
            abort(401, message="Patient doesn't have rights")
        abort(400, message='Invalid Intervention ID')
        # try:
        #     deleted_intervention = interventions.pop(intervention_id)
        #     return {'message':f'Intervention deleted for Patient ID# {deleted_intervention["patient_id"]}'}, 202
        # except KeyError:
        #     abort(404, message='Intervention not found')
# @app.delete('/intervention/<intervention_id>')
# def delete_intervention(intervention_id):
#     try:
#         store = interventions[intervention_id]['patient_id']
#         del interventions[intervention_id]
#     except KeyError:
#         return {'message': 'Intervention not found'}, 400
#     return {'message':f"Interventions have been deleted from database for Patient ID #{store}."}, 202
from flask import request
from uuid import uuid4
from flask.views import MethodView
from flask_smorest import abort

from schemas import InterventionSchema
from . import bp
from db import interventions


@bp.route('/')
class InterventionList(MethodView):
    def get(self):
        return {'interventions': interventions}
# @app.get('/intervention')
# def get_interventions():
#     return {'interventions': interventions}, 200

    @bp.arguments(InterventionSchema)
    def intervention(self, intervention_data):
        interventions[uuid4().hex] = intervention_data
        return intervention_data, 201
# @app.post('/intervention')
# def create_intervention():
#     intervention_data = request.get_json()
#     interventions[uuid4().hex] = intervention_data
#     return intervention_data, 201

@bp.route('/<post_id>')
class Intervention(MethodView):

    def get(self, intervention_id):
        try:
            intervention = interventions[intervention_id]
            return intervention, 200
        except KeyError:
            abort(404, message='Intervention Not Found')
      # return {'message': 'post not found'}, 400
# @app.get('/intervention/<intervention_id>')
# def get_intervention(intervention_id):
#     try:
#         intervention = interventions[intervention_id]
#         return intervention, 200
#     except KeyError:
#         return {'message': 'intervention not found'}, 400

    @bp.arguments(InterventionSchema)
    def put(self, intervention_data, intervention_id):
        if intervention_id in interventions:
            intervention = interventions[intervention_id]
            if intervention_data['intervention_id'] != intervention['intervention_id']:
                abort(400, message="Cannot edit other patient's intervention")
            intervention['modalities'] = intervention_data['modalities']
            intervention['AROM'] = intervention_data['AROM']
            intervention['PROM'] = intervention_data['PROM']
            intervention['strengthening'] = intervention_data['strengthening']
            return intervention, 200
        abort(404, message='Intervention not Found')
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

    def delete(self, intervention_id):
        try:
            deleted_intervention = interventions.pop(intervention_id)
            return {'message':f'Intervention deleted for Patient ID# {deleted_intervention["patient_id"]}'}, 202
        except KeyError:
            abort(404, message='Intervention not found')
# @app.delete('/intervention/<intervention_id>')
# def delete_intervention(intervention_id):
#     try:
#         store = interventions[intervention_id]['patient_id']
#         del interventions[intervention_id]
#     except KeyError:
#         return {'message': 'Intervention not found'}, 400
#     return {'message':f"Interventions have been deleted from database for Patient ID #{store}."}, 202
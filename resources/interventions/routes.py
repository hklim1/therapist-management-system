from flask import request
from uuid import uuid4

from app import app

from database import interventions

@app.get('/intervention')
def get_interventions():
    return {'interventions': interventions}, 200

@app.get('/intervention/<intervention_id>')
def get_intervention(intervention_id):
    try:
        intervention = interventions[intervention_id]
        return intervention, 200
    except KeyError:
        return {'message': 'intervention not found'}, 400

@app.post('/intervention')
def create_intervention():
    intervention_data = request.get_json()
    interventions[uuid4().hex] = intervention_data
    return intervention_data, 201

@app.put('/intervention/<intervention_id>')
def edit_post(intervention_id):
    intervention_data = request.get_json()
    if intervention_id in interventions:
        intervention = interventions[intervention_id]
        intervention['modalities'] = intervention_data['modalities']
        intervention['AROM'] = intervention_data['AROM']
        intervention['PROM'] = intervention_data['PROM']
        intervention['strengthening'] = intervention_data['strengthening']
        return intervention, 200
    return {'message': 'Intervention not found'}, 400

@app.delete('/intervention/<intervention_id>')
def delete_intervention(intervention_id):
    try:
        store = interventions[intervention_id]['patient_id']
        del interventions[intervention_id]
    except KeyError:
        return {'message': 'Intervention not found'}, 400
    return {'message':f"Interventions have been deleted from database for Patient ID #{store}."}, 202
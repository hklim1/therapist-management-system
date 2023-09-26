from flask import request
from uuid import uuid4

from app import app
from database import patients, interventions

@app.get('/patient')
def get_patients():
    return {'patients': patients}, 200

@app.get('/patient/<patient_id>')
def get_patient(patient_id):
    try:
        patient = patients[patient_id]
        return patient, 200
    except KeyError:
        return {'message':'patient not found'}, 400
    
@app.post('/patient')
def add_patient():
    patient_data = request.get_json()
    patients[uuid4().hex] = patient_data
    return patient_data, 201

@app.put('/patient/<patient_id>')
def update_patient(patient_id):
    patient_data = request.get_json()
    try:
        patient = patients[patient_id]
        patient['recovery week'] = patient_data['new recovery week']
        return patient, 200
    except KeyError:
        return {'message': 'patient not found'}, 400
    
@app.delete('/patient/<patient_id>')
def discharge_patient(patient_id):
    try:
        store = patients[patient_id]['name']
        del patients[patient_id]
    except KeyError:
        return {'message': 'patient not found'}, 400
    return {'message':f"{store} has been discharged and deleted from database"}, 202

@app.get('/patient/<patient_id>/interventions')
def get_patient_interventions(patient_id):
    if patient_id not in patients:
        return {'message': 'patient not found'}, 400
    return interventions[patient_id], 200
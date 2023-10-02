# from flask import request
from flask.views import MethodView
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from schemas import TherapistSchema, DeleteTherapistSchema, UpdateTherapistSchema, TherapistSchemaNested, AuthTherapistSchema
from . import bp
from .TherapistModel import TherapistModel
from flask_jwt_extended import jwt_required, get_jwt_identity

@bp.route('/therapist')
class TherapistList(MethodView):
    
    @bp.response(200, TherapistSchema(many = True))
    def get(self):
        therapists = TherapistModel.query.all()
        return therapists
    
    @bp.arguments(TherapistSchema)
    @bp.response(201, TherapistSchema)
    def post(self, therapist_data):
        therapist = TherapistModel()
        try:
            therapist.from_dict(therapist_data)
            therapist.save()
            return therapist_data
        except IntegrityError:
            abort(400, message='Therapist is already in system.')

    # @jwt_required()
    # @bp.arguments(AuthTherapistSchema)
    # def delete(self, therapist_data):
    #     therapist_id = get_jwt_identity()
    #     therapist = TherapistModel.query.get(therapist_id)
    #     if therapist and therapist.first_name == therapist_data['first_name'] and therapist.last_name == therapist_data['last_name'] and therapist.id == therapist_data['id']:
    #         therapist.delete()
    #         return {'message':f'{therapist_data["first_name"]} {therapist_data["last_name"]} has been deleted from system'}, 202
    #     abort(400, message='Therapist ID Invalid')
    @bp.arguments(DeleteTherapistSchema)
    def delete(self, therapist_data):
        print(therapist_data)
        therapist = TherapistModel.query.filter_by(id=therapist_data['id']).first()
        if therapist and therapist.last_name == therapist_data['last_name']:
            therapist.delete()
            return {'message':f'{therapist_data["first_name"]} {therapist_data["last_name"]} has been deleted.'}, 202
        abort(400, message='Therapist ID Invalid')

@bp.route('/therapist/<therapist_id>')
class Therapist(MethodView):

    @bp.response(200, TherapistSchemaNested)
    def get(self, therapist_id):
        therapist = TherapistModel.query.get_or_404(therapist_id, description='Therapist Not Found')
        return therapist
    
    @bp.arguments(UpdateTherapistSchema)
    @bp.response(202, UpdateTherapistSchema)
    def put(self, therapist_data, therapist_id):
        therapist = TherapistModel.query.get_or_404(therapist_id, description="Therapist Not Found")
        if therapist:
            try:
                therapist.from_dict(therapist_data)
                therapist.save()
                return therapist
            except IntegrityError:
                abort(400, message='Therapist already exists in system.')


@bp.route('/therapist/manage/<manager_id>/<employee_id>')
class MakeBoss(MethodView):
  
    @bp.response(200, TherapistSchema(many=True))
    def post(self, manager_id, employee_id):
        manager = TherapistModel.query.get(manager_id)
        employee = TherapistModel.query.get(employee_id)
        if manager and employee:
            manager.manage_employee(employee)
            return manager.manages.all()
        abort(400, message='Invalid therapist info')

    def put(self, manager_id, employee_id):
        manager = TherapistModel.query.get(manager_id)
        employee = TherapistModel.query.get(employee_id)
        if manager and employee:
            manager.stop_managing(employee)
            return {'message': f'{manager.first_name} {manager.last_name} no longer managing: {employee.first_name} {employee.last_name}'}, 202
        abort(400, message='Invalid therapist info')  
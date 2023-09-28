from marshmallow import Schema, fields

class InterventionSchema(Schema):
  id = fields.Str(dumps_only = True)
  modalities= fields.Str(required = True)
  AROM = fields.Str(required = True)
  PROM = fields.Str(required = True)
  strengthening = fields.Str(required = True)
  patient_id = fields.Str(required = True)

class PatientSchema(Schema):
  id = fields.Str(dumps_only = True)
  first_name = fields.Str(required = True)
  last_name = fields.Str(required = True)
  age = fields.Str()
  diagnosis = fields.Str(required = True)
  doi_dos = fields.Str()
  recovery_week = fields.Str()
  precautions = fields.Str()

class UpdatePatientSchema(Schema):
  first_name = fields.Str(required = True)
  last_name = fields.Str(required = True)
  age = fields.Str()
  diagnosis = fields.Str()
  doi_dos = fields.Str()
  recovery_week = fields.Str()
  precautions = fields.Str()

class DeletePatientSchema(Schema):
  id = fields.Str(dumps_only = True)
  first_name = fields.Str(required = True)
  last_name = fields.Str(required = True)
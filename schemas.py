from marshmallow import Schema, fields

class InterventionSchema(Schema):
  id = fields.Int(dump_only = True)
  modalities= fields.Str(required = True)
  AROM = fields.Str(required = True)
  PROM = fields.Str(required = True)
  strengthening = fields.Str(required = True)
  patient_id = fields.Int(required = True)
  # patient = fields.list(fields.Nested(PatientSchema()), dumps_only = True)
  # because of the above line, need to move class InterventionSchema below class PatientSchema since code runs top to bottom. Need to make sure the PatientSchema exists first.

class PatientSchema(Schema):
  id = fields.Int(dump_only = True)
  first_name = fields.Str(required = True)
  last_name = fields.Str(required = True)
  age = fields.Str()
  diagnosis = fields.Str(required = True)
  doi_dos = fields.Str()
  recovery_week = fields.Str()
  precautions = fields.Str()

class PatientSchemaNested(PatientSchema):
  interventions = fields.List(fields.Nested(InterventionSchema), dump_only=True)

class UpdateInterventionSchema(Schema):
  patient_id = fields.Int(required = True)
  modalities= fields.Str()
  AROM = fields.Str()
  PROM = fields.Str()
  strengthening = fields.Str()

class UpdatePatientSchema(Schema):
  first_name = fields.Str(required = True)
  last_name = fields.Str(required = True)
  age = fields.Str()
  diagnosis = fields.Str()
  doi_dos = fields.Str()
  recovery_week = fields.Str()
  precautions = fields.Str()

class DeletePatientSchema(Schema):
  id = fields.Int(load_only = True)
  first_name = fields.Str(required = True)
  last_name = fields.Str(required = True)

class TherapistSchema(Schema):
  id = fields.Int(dump_only = True)
  first_name = fields.Str(required = True)
  last_name = fields.Str(required = True)
  pt_ot = fields.Str(required = True)
  certifications = fields.Str()
  manager = fields.Bool()

class TherapistSchemaNested(TherapistSchema):
  manages = fields.List(fields.Nested(TherapistSchema), dump_only=True)

class UpdateTherapistSchema(Schema):
  first_name = fields.Str(required = True)
  last_name = fields.Str(required = True)
  pt_ot = fields.Str()
  certifications = fields.Str()
  manager = fields.Bool()

class DeleteTherapistSchema(Schema):
  id = fields.Int(load_only = True)
  first_name = fields.Str(required = True)
  last_name = fields.Str(required = True)

# class RelationshipSchema(Schema):
#   patient_id = fields.Int(required = True)
#   therapist_id = fields.Int(required = True)
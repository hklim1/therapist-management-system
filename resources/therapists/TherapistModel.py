from app import db

from werkzeug.security import generate_password_hash, check_password_hash

hierarchy = db.Table('hierarchy',
  db.Column('manager_id', db.Integer, db.ForeignKey('therapists.id')),
  db.Column('employee_id', db.Integer, db.ForeignKey('therapists.id'))           
)

class TherapistModel(db.Model):

  __tablename__  = 'therapists'

  id = db.Column(db.Integer, primary_key = True)
  first_name = db.Column(db.String, nullable = False)
  last_name = db.Column(db.String, nullable = False)
  pt_ot = db.Column(db.String, nullable = False)
  certifications = db.Column(db.String, nullable = True)
  manager = db.Column(db.Boolean, nullable = True)
  manages = db.relationship('TherapistModel', 
    secondary=hierarchy, 
    primaryjoin = hierarchy.c.manager_id == id,
    secondaryjoin = hierarchy.c.employee_id == id,
    backref = db.backref('managers', lazy='dynamic'),
    lazy='dynamic' 
  )

  def __repr__(self):
    return f'<Therapist {self.id}: {self.first_name} {self.last_name} >'
 
  def from_dict(self, dict):
    for k,v in dict.items():
      setattr(self, k, v)

  def save(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def is_established(self, therapist):
      return self.manages.filter(therapist.id == hierarchy.c.employee_id).count() > 0
  
  def manage_employee(self, therapist):
    if not self.is_established(therapist):
      self.manages.append(therapist)
      self.save()

  def stop_managing(self, therapist):
    if self.is_established(therapist):
      self.manages.remove(therapist)
      self.save()
from app import db

from werkzeug.security import generate_password_hash, check_password_hash

# We make these Model files to serve as our way of creating tables in SQL
# password_hash means user gives pw, werkzeug hashes it, passes us the hsahed pw. that way we dont have to store their sensitive data.

class PatientModel(db.Model):

  __tablename__  = 'patients'

# each class attribute = a table column
# every attribute value is a class of hteir own, specifies data type and constraints the data type might have (nullable, etc.)
  id = db.Column(db.Integer, primary_key = True) #primary_key = True means this is type SERIAL & will auto increment
  first_name = db.Column(db.String, nullable = False) # String ==VARCHAR in sqlalchemy
  last_name = db.Column(db.String, nullable = False) #by default nullable=true, nullable=false means it's required
  age = db.Column(db.String)
  diagnosis = db.Column(db.String, nullable = False)
  doi_dos = db.Column(db.String)
  recovery_week = db.Column(db.String)
  precautions = db.Column(db.String)

  def __repr__(self):
    return f'<Patient: {self.first_name} {self.last_name}'
  # this makes it easy to see who you are referencing when you type just "u" in the flask shell, so it turns the Object into something readable
  
  # def hash_password(self, password):
  #   self.password_hash = generate_password_hash(password)
  # the above is storing the hashed password into self.password_hash

  # def check_password(self, password):
  #   return check_password_hash(self.password_hash, password)
  # the above is checking the real pw input by the user to the hashed pw to make sure they match
  
  def from_dict(self, dict):
    # password = dict.pop('password')
    # self.hash_password(password)
    for k,v in dict.items():
      setattr(self, k, v)

  def save(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()
from app import db

from werkzeug.security import generate_password_hash, check_password_hash

# We make these Model files to serve as our way of creating tables in SQL
# password_hash means user gives pw, werkzeug hashes it, passes us the hsahed pw. that way we dont have to store their sensitive data.

# CREATING AN AUXILARY TABLE FOR MANY:MANY RELATIONSHIP. This is a table you can query off of, but it doesn't actually exist in the DB.

class PatientModel(db.Model):
  # db.Model - db is coming from app, where db is instance of SQLAlchemy instantiated with our app. SQLAlchemy. So this db.Model is specific to SQLAlchemy. SQLAlchemy is how we interact w/ db (e.g. creating tables, interacting with tables). That's why we create these classes with inheritance from db>model, so that a table is created in our db.
  # user = UserModel() = instance of a model AKA an entry, so you want to .save() and .commit()
  # Schemas utilize Marshmallow library - doesn't directly do anything w/ model. Use them when you are sending info to a route. "thanks to flask-smorest" we can validate information using marshmallow
  # Attributes in the Schemas must exactly match attributes in the Models "e.g. first_name == first_name"
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
  interventions = db.relationship('InterventionModel', backref='patient', lazy='dynamic', cascade='all, delete')

  def __repr__(self):
    return f'<Patient: {self.id}: {self.first_name} {self.last_name} >'
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

# class FollowerModel(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
#   following_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
# THIS IS ONE WAY TO DO A MANY TO MANY RELATIONSHIP. Even tho it's easier, it's not standard practice bc you are taking 2 FKs.
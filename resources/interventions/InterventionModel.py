from app import db

class InterventionModel(db.Model):
    
    __tablename__ = 'interventions'

    id = db.Column(db.Integer, primary_key = True)
    modalities = db.Column(db.String)
    AROM = db.Column(db.String)
    PROM = db.Column(db.String)
    strengthening = db.Column(db.String)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable = False)

    def __repr__(self):
        return f'<Interventions for: {self.patient_id}'
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
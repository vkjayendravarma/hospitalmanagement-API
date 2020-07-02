from src import db
from src.models import pharmacyModel,labModel

class Patient(db.Document):
    ssnid = db.StringField(max_length=9, unique=True)
    patientId = db.StringField()
    name = db.StringField( required=True )
    age=db.IntField(max_length=3)
    address=db.StringField()
    dateOfJoining= db.StringField()
    roomType=db.StringField()    
    pharmacy = db.ListField(db.StringField())
    diagnostics = db.ListField(db.StringField())
    status = db.StringField(default="active")
    
class config(db.Document):
    patientId = db.StringField()
    
    
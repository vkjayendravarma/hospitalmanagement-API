from src import db

class Patient(db.Document):
    ssnid = db.StringField(max_length=9, unique=True)
    name=db.StringField(max_length=9, )
    age=db.IntField(max_length=3)
    address=db.StringField()
    dateOfJoining= db.StringField()
    roomType=db.StringField()    
    pharmacy = []
    diagnostics = []
    
    
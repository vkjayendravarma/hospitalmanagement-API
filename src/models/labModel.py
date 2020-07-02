from src import db
import datetime
class LabInventory(db.Document):
    name=db.StringField()
    price=db.StringField()
    

class LabInvoice(db.Document):
    date = datetime.datetime.utcnow()
    items = db.ListField(db.ObjectIdField())
    total = db.StringField()
    
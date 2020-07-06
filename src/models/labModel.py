from src import db
import datetime
class LabInventory(db.Document):
    name=db.StringField()
    price=db.FloatField()
    

class LabInvoice(db.Document):
    date = db.DateTimeField(default=datetime.datetime.utcnow())
    items = db.ListField(db.ObjectIdField())
    total = db.FloatField()
    
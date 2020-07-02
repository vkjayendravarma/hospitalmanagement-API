from src import db
import time
class LabInventory(db.Document):
    name=db.StringField()
    price=db.StringField()
    

class LabInvoice(db.EmbeddedDocument):
    date = time.strftime("%H:%M:%S", time.localtime() ) 
    items = db.ListField(db.StringField())
    total = db.StringField()
    
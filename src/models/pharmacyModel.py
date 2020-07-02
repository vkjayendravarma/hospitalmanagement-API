from src import db
import datetime

class PahrmacyInventory(db.Document):
    name=db.StringField()
    quantity=db.IntField()
    price=db.FloatField()
    

class PharmacyInvoice(db.Document):
    date = db.DateTimeField(default=datetime.datetime.now)
    items = db.ListField(db.DictField())
    total = db.FloatField()
    
from src import db
import time

class PahrmacyInventory(db.Document):
    name=db.StringField()
    quantity=db.IntField()
    price=db.StringField()
    

class PharmacyInvoice(db.Document):
    date = time.strftime("%H:%M:%S", time.localtime() ) 
    items = []
    total = db.StringField()
    
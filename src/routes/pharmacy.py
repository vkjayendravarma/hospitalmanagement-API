from src import app,db,Config
from flask import request
from flask_mongoengine import mongoengine
from flask_api import status

from src.routes import shared
from src.models import pharmacyModel, patientModel

@app.route('/pharmacy/inventory/manageinventory', methods=['GET', 'POST'])
def getInventory(medicineID=None):
    #get all medicines
    if (request.method == 'GET'):
        data = pharmacyModel.PahrmacyInventory.objects()
        return {
                'success': True,
                'res': data
            }
    # new medicine
    if (request.method == 'POST'):
        try:
            name = request.form['name']
            quantity = int(request.form['quantity'])
            price = float(request.form['price'])
        except KeyError:
            return {
                'success': False,
                'message': 'missing fields'
            }, status.HTTP_400_BAD_REQUEST
        
        data = pharmacyModel.PahrmacyInventory(name= name, quantity= quantity, price = price).save()
        return {
                'success': True,
                'res': data
            }
        

            
# add medicions to stock
@app.route('/pharmacy/inventory/manageinventory/<medicineID>', methods=['PUT'])
def addSKU(medicineID):
    data = pharmacyModel.PahrmacyInventory.objects(id=medicineID).first()
    print(str(request.form['quantity']))
    
    quantityUpdate = data.quantity + int(request.form['quantity'])
    data.update(quantity=quantityUpdate)
    return {
        'success': True,
        'res': data
        }


@app.route('/pharmacy/patient/getpatientdata/<patientId>', methods=['GET'])
def pharmaGetPateient(patientId):
    data = patientModel.Patient.objects(patientId=patientId).first()
    if(data):
        pharmacyInvoices = shared.getPharmacyInvoices(data.pharmacy)
        data['pharmacy'] = pharmacyInvoices
        return {
            'success': True,
            'res': data
        }
    return {
        'success': False,
        'message': 'Patient not found'
    }
            
# new invoice to patients
@app.route('/pharmacy/patient/newinvoice/<patientID>', methods=['POST'])
def newinvoice(patientID):
    if(patientID):
        print(patientID)
        res = []
        invoice = []
        invoiceTotal = 0
        patient = patientModel.Patient.objects(patientId=patientID).first()
        if(patient):
            items = request.get_json()            
            for item in items['items']:
                medicine = pharmacyModel.PahrmacyInventory.objects(id=item['id']).first()
                if(medicine.quantity >= item['quantity']):
                    quantity = medicine.quantity - item['quantity']
                    medicine.update(quantity=quantity)
                    
                    invoiceTotal = invoiceTotal + (medicine.price * item['quantity'])
                    
                    invoice.append({'id' : medicine.id, 'quantity': item['quantity']})
                    
                else:
                    res.append({'name': medicine.name, 'qunantity': medicine.quantity})
            
            newInvoice = pharmacyModel.PharmacyInvoice( items=invoice, total = invoiceTotal).save()
            
            if (len(patient.pharmacy)>1):
                pharma =  patient.pharmacy               
                if(isinstance(pharma, str)):
                    print("string")
                    updatePatient = [patient.pharmacy, str(newInvoice['id'])]
                if(isinstance(pharma, list)):
                    print("list")
                    updatePatient = patient.pharmacy
                    updatePatient.append(str(newInvoice['id']))                                                                                          
                                        
                patient.update(pharmacy=updatePatient)
                
            else:                
                patient.update(pharmacy = str(newInvoice['id']))
                
            
            return {
                'success': True,
                'res': res
            }    
        else:
            return {
                'success': False,
                'message': 'No patient found'
            }, status.HTTP_404_NOT_FOUND
            


    
    


        
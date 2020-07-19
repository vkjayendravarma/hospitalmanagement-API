from src import app,db,Config
from flask import request
from flask_mongoengine import mongoengine
from flask_api import status

from src.routes import shared
from src.models import pharmacyModel, patientModel
from src.routes.security import authorization


@app.route('/pharmacy/inventory/manageinventory', methods=['GET', 'POST'])
@authorization
def getInventory(role,medicineID=None):
    L2Auth = role in ["HMAD", "HMLD"]
    if not L2Auth:
        return {
            "success": False,
            "message": "Unauthorized"
        },status.HTTP_401_UNAUTHORIZED
    #get all medicines
    if (request.method == 'GET'):
        data = pharmacyModel.PahrmacyInventory.objects()
        return {
                'success': True,
                'res': data
            }
    # new medicine
    if (request.method == 'POST'):
        req = request.get_json()
        try:
            name = req['name']
            quantity = int(req['quantity'])
            price = float(req['price'])
        except KeyError:
            return {
                'success': False,
                'message': 'missing fields'
            }, status.HTTP_400_BAD_REQUEST
        
        data = pharmacyModel.PahrmacyInventory(name= name, quantity= quantity, price = price).save()
        return {
                'success': True,
                'res': data
            },status.HTTP_200_OK
        

            
# add medicions to stock
@app.route('/pharmacy/inventory/manageinventory/<medicineID>', methods=['PUT'])
@authorization
def addSKU(role,medicineID):
    L2Auth = role in ["HMAD", "HMLD"]
    if not L2Auth:
        return {
            "success": False,
            "message": "Unauthorized"
        },status.HTTP_401_UNAUTHORIZED
    data = pharmacyModel.PahrmacyInventory.objects(id=medicineID).first()

    sku = request.get_json()

    quantityUpdate = data.quantity + int(sku)
    data.update(quantity=quantityUpdate)
    return {
        'success': True,
        'res': data
        },status.HTTP_200_OK


@app.route('/pharmacy/patient/getpatientdata/<patientId>', methods=['GET'])
@authorization
def pharmaGetPateient(role,patientId):
    L2Auth = role in ["HMAD", "HMLD"]
    if not L2Auth:
        return {
            "success": False,
            "message": "Unauthorized"
        },status.HTTP_401_UNAUTHORIZED
    data = patientModel.Patient.objects(patientId=patientId).first()
    if(data):
        pharmacyInvoices = shared.getPharmacyInvoices(data.pharmacy)
        data['pharmacy'] = pharmacyInvoices
        return {
            'success': True,
            'res': data
        },status.HTTP_200_OK
    return {
        'success': False,
        'message': 'Patient not found'
    },status.HTTP_404_NOT_FOUND
            
# new invoice to patients
@app.route('/pharmacy/patient/newinvoice/<patientID>', methods=['POST'])
@authorization
def newinvoice(role,patientID):
    L2Auth = role in ["HMAD", "HMLD"]
    if not L2Auth:
        return {
            "success": False,
            "message": "Unauthorized"
        },status.HTTP_401_UNAUTHORIZED
    if(patientID):
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
                    updatePatient = [patient.pharmacy, str(newInvoice['id'])]
                if(isinstance(pharma, list)):
                    updatePatient = patient.pharmacy
                    updatePatient.append(str(newInvoice['id']))                                                                                          
                                        
                patient.update(pharmacy=updatePatient)
                
            else:                
                patient.update(pharmacy = str(newInvoice['id']))
                
            
            return {
                'success': True,
                'res': res
            },status.HTTP_200_OK    
        else:
            return {
                'success': False,
                'message': 'No patient found'
            }, status.HTTP_404_NOT_FOUND
from src import app,db,Config
from flask import request
from flask_mongoengine import mongoengine
from flask_api import status

from src.models import labModel, patientModel

@app.route('/pharmacy/inventory/manageinventory', methods=['GET', 'POST'])
def getInventory(medicineID=None):
    #get all medicines
    if (request.method == 'GET'):
        data = labModel.LabInventory.objects()
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
        
        data = labModel.LabInventory(name= name, quantity= quantity, price = price).save()
        return {
                'success': True,
                'res': data
            }
        

            
# add medicions to stock
@app.route('/lab/inventory/manageinventory/<medicinID>', methods=['PUT'])
def addSKU(medicineID):
    data = labModel.LabInventory.objects(id=medicineID).first()
    quantityUpdate = data.quantity + int(request.form['quantity'])
    data.update(quantity=quantityUpdate)
    return {
        'success': True,
        'res': data
        }
            
# new invoice to patients
@app.route('/lab/patient/newinvoice/<patientID>', methods=['POST'])
def newinvoice(patientID):
    if(patientID):
        print(patientID)
        res = []
        invoice = []
        invoiceTotal = 0
        patient = patientModel.Patient.objects(patientId=patientID).first()
        if(patient):
            items = request.get_json()            
                
            newInvoice = labModel.LabInvoice(items=invoice, total = invoiceTotal).save()
            
            if (len(patient.diagnostics)>1):
                pharma =  patient.diagnostics               
                if(isinstance(pharma, str)):
                    print("string")
                    updatePatient = [patient.diagnostics, str(newInvoice['id'])]
                if(isinstance(pharma, list)):
                    print("list")
                    updatePatient = patient.diagnostics
                    updatePatient.append(str(newInvoice['id']))                                                                                          
                                        
                patient.update(diagnostics=updatePatient)
                
            else:                
                patient.update(diagnostics = str(newInvoice['id']))
                
            
            return {
                'status': True,
                'res': res
            }    
        else:
            return {
                'success': False,
                'message': 'No patient found'
            }, status.HTTP_404_NOT_FOUND
            


    
    


        
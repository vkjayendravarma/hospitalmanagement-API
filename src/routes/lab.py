from src import app,db,Config
from flask import request
from flask_mongoengine import mongoengine
from flask_api import status

from src.routes import shared
from src.models import patientModel, labModel

@app.route('/lab/inventory/manageinventory', methods=['GET', 'POST'])
def getLabInventory(medicineID=None):
    #get all tests
    if (request.method == 'GET'):
        data = labModel.LabInventory.objects()
        return {
                'success': True,
                'res': data
            }
    # new test
    if (request.method == 'POST'):
        try:
            name = request.form['name']
            price = float(request.form['price'])
        except KeyError:
            return {
                'success': False,
                'message': 'missing fields'
            }, status.HTTP_400_BAD_REQUEST
        
        data = labModel.LabInventory(name= name, price = price).save()
        return {
                'success': True,
                'res': data
            }


@app.route('/lab/patient/getpatientdata/<patientId>', methods=['GET'])
def labGetPateient(patientId):
    data = patientModel.Patient.objects(patientId=patientId).first()
    if(data):
        labInvoices = shared.getLabInvoices(data.diagnostics)
        data['diagnostics'] = labInvoices
        return {
            'success': True,
            'res': data
        }
    return {
        'success': False,
        'message': 'Patient not found'
    }


# new invoice to patients
@app.route('/lab/patient/newinvoice/<patientID>', methods=['POST'])
def newLabinvoice(patientID):
    if(patientID):
        print(patientID)
        res = []
        invoice = []
        invoiceTotal = 0
        patient = patientModel.Patient.objects(patientId=patientID).first()
        if(patient):
            items = request.get_json()            
            for item in items['items']:
                labTest = labModel.LabInventory.objects(id=item).first()
                invoice.append(labTest.id)
                invoiceTotal = invoiceTotal + labTest.price               
            
            newInvoice = labModel.LabInvoice( items=invoice, total = invoiceTotal).save()
            
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
                'message': "Invocice generated"
            }    
        
        return {
            'success': False,
            'message': 'No patient found'
        }, status.HTTP_404_NOT_FOUND
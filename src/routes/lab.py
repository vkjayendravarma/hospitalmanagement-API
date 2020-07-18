from src import app,db,Config
from flask import request
from flask_mongoengine import mongoengine
from flask_api import status

from src.routes import shared
from src.models import patientModel, labModel
from src.routes.security import authorization


@app.route('/lab/inventory/manageinventory', methods=['GET', 'POST'])
@authorization
def getLabInventory(role,medicineID=None):
    L2Auth = role in ["HMAD", "HMLD"]
    if not L2Auth:
        return {
            "success": False,
            "message": "Unauthorized"
        }
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


@app.route('/lab/patient/getpatientdata', methods=['GET'])
@authorization
def labGetPateient(role):
    L2Auth = role in ["HMAD", "HMLD"]
    if not L2Auth:
        return {
            "success": False,
            "message": "Unauthorized"
        }
    patientId = request.args['patientId']
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
@app.route('/lab/patient/newinvoice', methods=['POST'])
@authorization
def newLabinvoice(role):
    L2Auth = role in ["HMAD", "HMLD"]
    if not L2Auth:
        return {
            "success": False,
            "message": "Unauthorized"
        }
    patientID = request.args['patientId']
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
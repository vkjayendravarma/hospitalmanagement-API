from src import app,db,Config
from flask import request
from src.models import patientModel
from flask_mongoengine import mongoengine
from flask_api import status

from src.routes import shared

@app.route('/reception/patients/new',methods=['POST'])
def newPatient():
    try:
        ssnid = request.form['ssnid']
        name=request.form['name']
        age= int(request.form['age'])
        address= request.form['address']
        dateOfJoining= request.form['dateOfJoining']
        roomType= request.form['roomType'] 
    except KeyError:
        return {"success": False, "message": "one or more missing fields"}, status.HTTP_400_BAD_REQUEST
    
    patientId = str(100000000 + patientModel.Patient.objects().count())
    patient = patientModel.Patient(ssnid=ssnid,patientId=patientId, name=name, age =age, address=address, dateOfJoining=dateOfJoining, roomType=roomType).save()
    patientid = str(patient['patientId'])
    return {
        'success': True,
        'res': {            
            'message': 'patient created',
            'patientId': patientid            
        }
    }
    
@app.route('/reception/patients',methods=['GET'])
def allPatients():
    data = patientModel.Patient.objects()
    return {
        'success': True,
        'res': data
    }
    
# GET return patient data
# POST update patient data
# PUT change status to Discharged
# DELETE delete patient
    
@app.route('/reception/patients/<patientId>', methods=['GET', 'PUT','POST', 'DELETE'])
def Patient(patientId):
    
    if request.method == 'GET':
        data = patientModel.Patient.objects(patientId=patientId).first()        
        pharmacyInvoices = shared.getPharmacyInvoices(data.pharmacy)
        data['pharmacy'] = pharmacyInvoices
        return {
            'success': True,
            'res': data
        }
        
    if request.method == 'POST':
        data = patientModel.Patient.objects(patientId=patientId)
        if(data):
            print(data)
            try:
                ssnid = request.form['ssnid']
                name=request.form['name']
                age= int(request.form['age'])
                address= request.form['address']
                dateOfJoining= request.form['dateOfJoining']
                roomType= request.form['roomType'] 
            except KeyError:
                return {"success": False, "message": "one or more missing fields"}, status.HTTP_400_BAD_REQUEST
            
            data.update(ssnid=ssnid,patientId=patientId, name=name, age =age, address=address, dateOfJoining=dateOfJoining, roomType=roomType)
        else:
            return "False"
        
        return {
            'success': True,
            'message': 'updated'
        }
        
    if(request.method == 'PUT'):
        data = patientModel.Patient.objects(patientId=patientId)
        data.update(status = 'Discharged')
        
        return {
            'success': True,
            'message': 'patient discharged'
        }
    
    if(request.method == 'DELETE'):
        data = patientModel.Patient.objects(patientId=patientId)
        data.delete()
        
        return {
            'success': True,
            'message': 'deleted'
        }
        
        
        
    

    
        
    
from src import app,db,Config
from flask import request
from src.models import patientModel
from flask_mongoengine import mongoengine
from flask_api import status


@app.route('/reception/patient/new',methods=['POST'])
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

    patient = patientModel.Patient(ssnid=ssnid, name=name, age =age, address=address, dateOfJoining=dateOfJoining, roomType=roomType).save()
    patientid = str(patient['id'])
    return {
        'success': True,
        'res': {            
            'message': 'patient created',
            'patientId': patientid            
        }
    }
    
@app.route('/reception/patient',methods=['GET'])
def allPatients():
    data = patientModel.Patient.objects()
    return {
        'success': True,
        'res': data
    }

    
        
    
from src import app, db, Config
from flask import request
from src.models import patientModel
from flask_mongoengine import mongoengine
from flask_api import status

from src.routes import shared


@app.route('/reception/patients/new', methods=['POST'])
def newPatient():
    req = dict(request.get_json())
   
    try:
        ssnid = req['ssnid']
        name = req['name']
        age = int(req['age'])
        address = req['address']
        dateOfJoining = req['dateOfJoining']
        roomType = req['roomType']
        city = req['city']
        state = req['state']
    except KeyError as e:
        print(str(e))
        return "Null"

    patientId = str(100000000 + patientModel.Patient.objects().count())
    try:
        patient = patientModel.Patient(ssnid=ssnid, patientId=patientId, name=name, age=age, address=address, dateOfJoining=dateOfJoining, roomType=roomType, city=city, state=state).save()
        patientid = str(patient['patientId'])
    except mongoengine.errors.NotUniqueError as e:
        return {'success': False, 'message': "SSN ID exists"}
    except mongoengine.errors.ValidationError as e:
        return {'success': False, 'message': "Missing field"}

    return {
        'success': True,
        'res': {
            'message': 'patient created',
            'patientId': patientid
        }
    }

# return all patients


@app.route('/reception/patients', methods=['GET'])
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


@app.route('/reception/patients/individual/<patientId>', methods=['GET', 'PUT', 'POST', 'DELETE'])
def Patient(patientId):

    if request.method == 'GET':
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

    if request.method == 'POST':
        data = patientModel.Patient.objects(patientId=patientId)
        if(data):
            print(data)
            req = request.get_json()
            

            try:
                ssnid = req['ssnid']
                name = req['name']
                age = int(req['age'])
                address = req['address']
                dateOfJoining = req['dateOfJoining']
                roomType = req['roomType']

            except KeyError:
                return {"success": False, "message": "one or more missing fields"}, status.HTTP_400_BAD_REQUEST

            data.update(ssnid=ssnid, patientId=patientId, name=name, age=age,
                        address=address, dateOfJoining=dateOfJoining, roomType=roomType)
        else:
            return {
                'success': False,
                'message': 'Patient not found'
            }

        return {
            'success': True,
            'message': 'updated'
        }

    if(request.method == 'PUT'):
        data = patientModel.Patient.objects(patientId=patientId)
        if(data):
            data.update(status='Discharged')

            return {
                'success': True,
                'message': 'patient discharged'
            }
        else:
            return {
                'success': False,
                'message': 'Patient not found'
            }

    if(request.method == 'DELETE'):
        data = patientModel.Patient.objects(patientId=patientId)

        if(data):
            data.delete()

            return {
                'success': True,
                'message': 'deleted'
            }
        else:
            return {
                'success': False,
                'message': 'Patient not found'
            }

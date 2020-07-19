from src import app,db,Config
from flask import request
from flask_api import status
from src.models import usersModel
from flask_mongoengine import mongoengine
import bcrypt
import jwt
import datetime
from src.routes.security import authorization



@app.route('/register', methods=['POST'])
@authorization
def register(role):
    if role != 'HMAD':
        return {
            'success': False,
            'message': 'Unauthorized'
        },status.HTTP_401_UNAUTHORIZED
    req =request.get_json()
    try:
        name = req['name']
        email = req['email']
        password = req['password'].encode("UTF-8")
        dept = req['dept']
    except KeyError as e:
        return {"success": False, "message": "one or more missing fields"}, status.HTTP_400_BAD_REQUEST
    
    
    password = bcrypt.hashpw(password, bcrypt.gensalt())
    
    try:        
        usersModel.User(name=name, email=email, password=password, dept=dept).save()
    except mongoengine.errors.NotUniqueError as e:
        return {
            'success': False,
            'message': 'User exists'
        }, status.HTTP_403_FORBIDDEN
    
    return {
        'success': True,
        'message': 'User Created'
    }, status.HTTP_200_OK

@app.route('/login', methods=['POST'])
def login():
    email= request.form['email']
    password= request.form.get('password').encode("UTF-8")
    
    user = usersModel.User.objects(email=email).first()
    if(user):

        if(bcrypt.checkpw(password, user.password.encode("UTF-8"))):
            token = jwt.encode({'user': str(user['id']), "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, Config.SECRET_KEY)
            return {
                "success": True,
                "token": token.decode('UTF-8') + user['dept']              
            },status.HTTP_200_OK
        else:
            return {
                "success": False,
                "message": "Invalid password"
            }, status.HTTP_403_FORBIDDEN
        
    else:
        return {
                "success": False,
                "message": "User not found"
            }, status.HTTP_404_NOT_FOUND
		
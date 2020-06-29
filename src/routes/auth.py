from src import app,db
from flask import request
from src.models import usersModel
from flask_mongoengine import mongoengine
import bcrypt



@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form.get('password').encode("UTF-8")
    accessLevel = request.form['accessLevel']
    
    password = bcrypt.hashpw(password, bcrypt.gensalt())
    
    try:        
        usersModel.User(name=name, email=email, password=password, accessLevel=accessLevel).save()
    except mongoengine.errors.NotUniqueError as e:
        print(e)
        return str(e)
    
    return "None"

@app.route('/login', methods=['POST'])
def login():
    email= request.form['email']
    password= request.form.get('password').encode("UTF-8")
    
    user = usersModel.User.objects(email=email).first()
    if(user):
        if(bcrypt.checkpw(password, user.password.encode("UTF-8"))):
            return {
                "success": True,
                "res": {
                    "name": user.name,
                    "accessLevel": user.accessLevel
                }
                
                }
        else:
            return "failed"
        
    else:
        return "No"
		
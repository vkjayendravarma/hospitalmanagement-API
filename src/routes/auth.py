from src import app
from flask import request

@app.route('/', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    print (email + password)
       
    return {
        "success": True,
        "res": {
            "email": email,
            "password": password
        }
    }
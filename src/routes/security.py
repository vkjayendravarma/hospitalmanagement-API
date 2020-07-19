from functools import wraps
from config import Config
import jwt
from flask import request
from flask_api import status
from src.models import usersModel
from flask_mongoengine import mongoengine

def roleCheck(id, role):
    user = usersModel.User.objects(id=id).first()
    if user.dept != role:
        return False
    return True


def authorization(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if 'Authorization' in request.headers:
            auth = request.headers['Authorization']
            token = auth[:-4]
            role =  auth[-4:]            
            try:
                decode = jwt.decode(token, Config.SECRET_KEY)                                    
            except jwt.exceptions.DecodeError as ex:
                print (ex)
                return {
                    'success': False,
                    'message': 'invalid token'
                },status.HTTP_401_UNAUTHORIZED
            except jwt.exceptions.InvalidTokenError as ex:
                print (ex)
                return {
                    'success': False,
                    'message': 'invalid token'
                },status.HTTP_401_UNAUTHORIZED
            except jwt.exceptions.InvalidSignatureError as ex:
                print (ex)
                return {
                    'success': False,
                    'message': 'invalid token'
                },status.HTTP_401_UNAUTHORIZED
            except jwt.exceptions.ExpiredSignatureError as ex:
                print (ex)
                return {
                    'success': False,
                    'message': 'invalid token'
                },status.HTTP_401_UNAUTHORIZED
            except jwt.exceptions.InvalidAudienceError as ex:
                print (ex)
                return {
                    'success': False,
                    'message': 'invalid token'
                },status.HTTP_401_UNAUTHORIZED
            except jwt.exceptions.InvalidIssuerError as ex:
                print (ex)
                return {
                    'success': False,
                    'message': 'invalid token'
                },status.HTTP_401_UNAUTHORIZED
            except jwt.exceptions.InvalidIssuedAtError as ex:
                print (ex)
                return {
                    'success': False,
                    'message': 'invalid token'
                },status.HTTP_401_UNAUTHORIZED
            except jwt.exceptions.ImmatureSignatureError as ex:
                print (ex)
                return {
                    'success': False,
                    'message': 'invalid token'
                },status.HTTP_401_UNAUTHORIZED
            except jwt.exceptions.InvalidKeyError as ex:
                print (ex)
                return {
                    'success': False,
                    'message': 'invalid token'
                },status.HTTP_401_UNAUTHORIZED
            except jwt.exceptions.InvalidAlgorithmError as ex:
                print (ex)
                return {
                    'success': False,
                    'message': 'invalid token'
                },status.HTTP_401_UNAUTHORIZED
            except jwt.exceptions.MissingRequiredClaimError as ex:
                print (ex)
                return {
                    'success': False,
                    'message': 'invalid token'
                },status.HTTP_401_UNAUTHORIZED
            if not roleCheck(decode['user'],role):
                return {
                    'success': False,
                    'message': 'Unauthorised'
                },status.HTTP_401_UNAUTHORIZED
           
        else:        
            return {
                'success': False,
                'message': 'Unauthorised'
            }, status.HTTP_403_FORBIDDEN
        return func(role, *args, **kwargs)
    return decorated
    
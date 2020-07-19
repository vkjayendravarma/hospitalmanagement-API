import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kaslhfkasdbviahkvbasivhaknviashflsdajcaiojalkbfiawhwcnaihv'
    MONGODB_SETTINGS = {
        'db': 'hospitalManagement',
        'host': '***___****'
    }

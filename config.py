import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kaslhfkasdbviahkvbasivhaknviashflsdajcaiojalkbfiawhwcnaihv'
    MONGODB_SETTINGS = {
        'db': 'hospitalManagement',
        'host': 'mongodb+srv://casestudyapi:pass123$@tcs-e7psm.mongodb.net/tcsCaseStudy'
    }
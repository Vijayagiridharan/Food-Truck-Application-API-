# config file for flask app
#import os


#class Config:
    #SECRET_KEY = os.getenv('SECRET_KEY', 'a_default_secret')
    #SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///default.db')


class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://username:password@localhost/databasename'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

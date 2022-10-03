import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

def database(mode=''):
    database_user = os.environ.get('DB_USER'+mode)
    database_user_password = os.environ.get('DB_PASSWORD'+mode)
    database_name = os.environ.get('DB_NAME'+mode)
    database_host = os.environ.get('DB_HOST'+mode)
    database_port = os.environ.get('DB_PORT'+mode)
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
        database_user, database_user_password, database_host, database_port, database_name
    )

    return SQLALCHEMY_DATABASE_URI

class Config(object):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'no secret key')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = database()
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = database('_TEST')

class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = 'production'
    SQLALCHEMY_DATABASE_URI = database('_PROD')

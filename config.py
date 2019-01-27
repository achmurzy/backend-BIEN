import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    #SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    POSTGRES = {
        'user': 'bien',
        'passw': 'bien',
        'host': 'localhost',
        'port': '5433',
        'name': 'vegbien', 
    }
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://%(user)s:%(passw)s@%(host)s:%(port)s/%(name)s" % POSTGRES

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
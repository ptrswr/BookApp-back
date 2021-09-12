import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class BaseConf(object):
    ORIGINS = ["*"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConf(BaseConf):
    DEBUG = True
    TESTING = False
    ENV = "development"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "book_database.db")
    APPNAME = "BookApp"


class TestingConfig(BaseConf):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    ENV = "testing"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "book_test.db")
    DEBUG = True

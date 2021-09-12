import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CSV_FOR_TESTS = "test_books.csv"

class BaseConf(object):
    ORIGINS = ["*"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConf(BaseConf):
    DEBUG = True
    ENV = "development"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "book_database.db")
    APPNAME = "BookApp"


class TestingConfig(BaseConf):
    """Configurations for Testing, with a separate test database."""
    ENV = "testing"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "book_test.db")
    DEBUG = True

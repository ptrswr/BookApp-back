from api import app
from api.config import DevelopmentConf


if __name__ == '__main__':
    book_app = app.create_app(DevelopmentConf)
    book_app.run()




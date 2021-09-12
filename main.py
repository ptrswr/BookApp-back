from api import app
import config


if __name__ == '__main__':
    book_app = app.create_app(config.DevelopmentConf)
    book_app.run()




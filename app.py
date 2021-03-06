from flask import Flask
from flask_cors import CORS
from books_stash import book_stash
from book_model import db
from config import DevelopmentConf


def create_app(conf):
    app = Flask(__name__)
    app.config.from_object(conf)
    db.init_app(app)
    CORS(app)
    with app.app_context():
        db.create_all()
        db.session.commit()
    app.register_blueprint(book_stash)
    return app


if __name__ == '__main__':
    app = create_app(DevelopmentConf)
    app.run()

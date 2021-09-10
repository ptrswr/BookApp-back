from flask import Flask
from flask_cors import CORS
from books_stash import book_stash
from book_model import db, database_file


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_file
    db.init_app(app)
    CORS(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()
    app.register_blueprint(book_stash)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()

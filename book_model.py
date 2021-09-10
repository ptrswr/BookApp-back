import datetime
import os
from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "book_database.db"))

db = SQLAlchemy()


@dataclass
class Book(db.Model):
    __tablename__ = 'books'

    book_id: int
    title: str
    author: str
    publish_date: datetime.datetime
    isbn_num: int
    page_count: int
    cover_link: str
    language: str

    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    publish_date = db.Column(db.DateTime)
    isbn_num = db.Column(db.String)
    page_count = db.Column(db.Integer)
    cover_link = db.Column(db.String)
    language = db.Column(db.String)

    def __init__(self, title, author, publish_date, isbn_num, page_count, cover_link, language):
        self.title = title
        self.author = author
        self.publish_date = publish_date
        self.isbn_num = isbn_num
        self.page_count = page_count
        self.cover_link = cover_link
        self.language = language

    def __repr__(self):
        return '<Book> Title {} Author{} Publish Date{} ISBN {}  Page Count {} Cover Link {} Language {}'.format(
            self.title, self.author, self.publish_date, self.isbn_num, self.page_count, self.cover_link, self.language)

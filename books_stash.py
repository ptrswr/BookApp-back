import json

from flask import request, jsonify, Blueprint
from sqlalchemy.exc import SQLAlchemyError

from book_model import Book
from book_model import db
import datetime as dt

book_stash = Blueprint('book_stash', __name__)


@book_stash.route('/api/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify({'data': books})


@book_stash.route('/api/books/<id>', methods=['GET'])
def get_book_by_id(id):
    books = Book.query.filter_by(book_id=id).first()
    return jsonify({'data': books})


@book_stash.route('/api/books/<query_type>/<query_field>', methods=['GET'])
def get_books_by_query(query_type, query_field):
    if query_type == 'author':
        books = Book.query.filter_by(author=query_field).all()
    elif query_type == 'title':
        books = Book.query.filter_by(title=query_field).all()
    elif query_type == 'language':
        books = Book.query.filter_by(language=query_field).all()
    else:
        return jsonify({'msg': 'Incorrect query string'}), 409

    return jsonify({'data': books})


@book_stash.route('/api/books/<date_start>/<date_end>', methods=['GET'])
def get_books_by_dates(date_start, date_end):
    if not date_start or not date_end:
        return jsonify({'msg': 'No dates'}), 409

    books = Book.query.filter(Book.publish_date.between(date_start, date_end)).all()
    return jsonify({'data': books})


@book_stash.route('/api/books/delete/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    print(book_id)
    book = Book.query.filter_by(book_id=book_id).first()
    if not book:
        return jsonify({'msg': 'There is no book with given id'}), 409
    try:
        db.session.delete(book)
        db.session.commit()
    except:
        return jsonify({"msg": "Database delete error"}), 500
    return jsonify({'msg': f'Book {book.title} was deleted'}), 200


@book_stash.route('/api/books/edit/<book_id>', methods=['PUT'])
def edit_book(book_id):
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    print(book_id)
    book = Book.query.filter_by(book_id=book_id).first()
    if not book:
        return jsonify({'msg': 'There is no book with given id'}), 409

    title = request.json.get('title', None)
    author = request.json.get('author', None)
    publish_date = dt.datetime.strptime(request.json.get('publish_date', None), '%Y-%m-%d')
    isbn_num = request.json.get('isbn_num', None)
    page_count = request.json.get('page_count', None)
    cover_link = request.json.get('cover_link', None)
    language = request.json.get('language', None)

    try:
        book.title = title
        book.author = author
        book.publish_date = publish_date
        book.isbn_num = isbn_num
        book.page_count = page_count
        book.cover_link = cover_link
        book.language = language
        db.session.commit()
    except:
        return jsonify({"msg": "Database write error"}), 500
    return jsonify({'msg': f'Book {book.title} was changed'}), 200


@book_stash.route('/api/books/add', methods=['POST'])
def add_book():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    title = request.json.get('title', None)
    author = request.json.get('author', None)
    publish_date = dt.datetime.strptime(request.json.get('publish_date', None), '%Y-%m-%d')
    isbn_num = request.json.get('isbn_num', None)
    page_count = request.json.get('page_count', None)
    cover_link = request.json.get('cover_link', None)
    language = request.json.get('language', None)

    new_book = Book(title, author, publish_date, isbn_num, page_count, cover_link, language)
    try:
        db.session.add(new_book)
        db.session.commit()

    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return jsonify({"msg": "Database write error"}), 500

    return jsonify({'msg': 'New book added'}), 200


@book_stash.route('/api/books/import', methods=['POST'])
def import_book_from_google():
    response = request.json.get('data')
    book_list = json.loads(response)
    books_to_add = []
    for book in book_list:
        title = book['title']
        author = book['author']
        publish_date = dt.datetime.strptime(book['publish_date'], '%Y-%m-%d')
        isbn_num = book['isbn_num']
        page_count = book['page_count']
        cover_link = book['cover_link']
        language = book['language']

        new_book = Book(title, author, publish_date, isbn_num, page_count, cover_link, language)
        books_to_add.append(new_book)

    try:
        db.session.bulk_save_objects(book_list)
        db.session.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return jsonify({"msg": "Database write error"}), 500

    return jsonify({'msg': 'New book added'}), 200
#  {
#             "title":"Eloquent JavaScript, Third Edition",
#             "author":"Marijn Haverbeke",
#             "publish_date":"2018-12-04T00:00:00.000Z",
#             "isbn_num":"9781593279509",
#             "page_count": 4567,
#             "cover_link":"http://eloquentjavascript.net/",
#             "language":"English"
# },

import json

from dateutil.parser import parse
from flask import request, jsonify, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from book_model import Book
from book_model import db

book_stash = Blueprint('book_stash', __name__)


@book_stash.route('/api/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify({'data': books})


@book_stash.route('/api/books/<book_id>', methods=['GET'])
def get_book_by_id(book_id):
    books = Book.query.filter_by(book_id=book_id).first()
    return jsonify({'data': books})


@book_stash.route('/api/books/search', methods=['GET'])
def search_by_qstring():
    q_string = request.args.get('q').split()
    q_params = []
    query = Book.query
    for q in q_string:
        q_params.append(q.split(':'))
    for param in q_params:
        if param[0] == "author":
            query = query.filter(Book.author == param[1])
        elif param[0] == "title":
            query = query.filter(Book.title == 'Hobbit')
        elif param[0] == "publishDate":
            query = query.filter(Book.publish_date == param[1])
        elif param[0] == "isbnNum":
            query = query.filter(Book.isbn_num == param[1])
        elif param[0] == "pageCount":
            query = query.filter(Book.page_count == param[1])
        elif param[0] == "coverLink":
            query = query.filter(Book.cover_link == param[1])
        elif param[0] == "language":
            query = query.filter(Book.language == param[1])

    books = query.all()
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


@book_stash.route('/api/books/delete/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    print(book_id)
    book = Book.query.filter_by(book_id=book_id).first()
    if not book:
        return jsonify({'msg': 'There is no book with given id'}), 409
    try:
        db.session.delete(book)
        db.session.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return jsonify({"msg": "Database write error"}), 500
    return jsonify({'msg': f'Book {book.title} was deleted'}), 200


@book_stash.route('/api/books/edit/<book_id>', methods=['PUT'])
def edit_book(book_id):
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    book = Book.query.filter_by(book_id=book_id).first()
    if not book:
        return jsonify({'msg': 'There is no book with given id'}), 409

    book.title = request.json.get('title', None)
    book.author = request.json.get('author', None)
    book.publish_date = request.json.get('publish_date', None)
    book.isbn_num = request.json.get('isbn_num', None)
    book.page_count = request.json.get('page_count', None)
    book.cover_link = request.json.get('cover_link', None)
    book.language = request.json.get('language', None)

    try:
        db.session.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return jsonify({"msg": "Database write error"}), 500
    return jsonify({'msg': f'Book {book.title} was changed'}), 200


@book_stash.route('/api/books/add', methods=['POST'])
def add_book():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    new_book = Book(request.json.get('title', None),
                    request.json.get('author', None),
                    request.json.get('publish_date', None),
                    request.json.get('isbn_num', None),
                    request.json.get('page_count', None),
                    request.json.get('cover_link', None),
                    request.json.get('language', None))
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
    books_to_add = []
    for book in response:
        new_book = Book(book['title'],
                        book['author'],
                        book['publish_date'],
                        book['isbn_num'],
                        book['page_count'],
                        book['cover_link'],
                        book['language'])
        books_to_add.append(new_book)

    try:
        db.session.bulk_save_objects(books_to_add)
        db.session.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return jsonify({"msg": "Database write error"}), 500

    return jsonify({'msg': 'Books imported'}), 200
#  {
#             "title":"Eloquent JavaScript, Third Edition",
#             "author":"Marijn Haverbeke",
#             "publish_date":"2018-12-04T00:00:00.000Z",
#             "isbn_num":"9781593279509",
#             "page_count": 4567,
#             "cover_link":"http://eloquentjavascript.net/",
#             "language":"English"
# },

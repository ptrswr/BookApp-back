import unittest
import json
from api.config import *
from api.app import create_app, db
from api.book_model import Book


class TestBase(unittest.TestCase):
    app_test = None
    app = None

    @classmethod
    def setUpClass(cls):
        cls.app = create_app(TestingConfig)
        cls.app_test = cls.app.test_client()
        cls.app.app_context().push()
        db.drop_all()
        db.create_all()
        db.session.commit()

    def test_AA_populate_db(self):
        response = self.app_test.get('/api/books/populate')
        self.assertEqual(response.status_code, 200)




class TestModels(TestBase):

    def test_get_all_books(self):
        response = self.app_test.get('/api/books')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data['data']), 3)
        self.assertEqual(response.status_code, 200)


class TestApiTests(TestBase):

    def test_add_book(self):
        response = self.app_test.post('/api/books/add',
                                      json={
                                          "title": "Test 3",
                                          "author": "Test Author 3",
                                          "publish_date": "03/03/1999",
                                          "isbn_num": "4124242142421",
                                          "page_count": 2500,
                                          "cover_link": "blank.com",
                                          "language": "english",

                                      })
        self.assertEqual(response.status_code, 200)

    def test_add_many_books(self):
        response = self.app_test.post('/api/books/import',
                                      json={"data": [
                                          {
                                              "title": "Test 4",
                                              "author": "Test Author 4",
                                              "publish_date": "03/03/1999",
                                              "isbn_num": "4124242142421",
                                              "page_count": 2500,
                                              "cover_link": "blank.com",
                                              "language": "english",

                                          },
                                          {
                                              "title": "Eloquent JavaScript, Third Edition",
                                              "author": "Marijn Haverbeke",
                                              "publish_date": "2018-12-04T00:00:00.000Z",
                                              "isbn_num": "9781593279509",
                                              "page_count": 4567,
                                              "cover_link": "http://eloquentjavascript.net/",
                                              "language": "English"
                                          }
                                      ]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.query.count(), 6)

    def test_delete_book(self):
        response = self.app_test.delete('/api/books/delete/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.query.count(), 5)

    def test_edit_non_existing_book(self):
        response = self.app_test.put('/api/books/edit/9', json={})
        self.assertEqual(response.status_code, 409)

    def test_edit_book_no_json(self):
        response = self.app_test.put('/api/books/edit/1')
        self.assertEqual(response.status_code, 400)

    def test_query_string_search(self):
        response = self.app_test.get('/api/books/search?q=title:Test 1')
        book_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(book_data['data'][0]['title'], 'Test 1')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

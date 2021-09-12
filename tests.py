import unittest
import json
from config import *
from app import create_app, db





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

#
# class TestAddEdit(TestBase):
#
#     def test_add_fragment(self):
#         response = self.app_test.post('/api/fragments/add',
#                                       json={
#                                           "area_id": 1,
#                                           "point_start": 1,
#                                           "point_end": 2,
#                                           "name": "Odcinek 1",
#                                           "length": 2500,
#                                           "scoring_up": 8,
#                                           "scoring_down": 3,
#                                           "climb_length": 600,
#                                           "fragment_type": "punktowany"
#                                       },
#                                       headers={'Authorization': 'Bearer ' + self.token})
#         self.assertEqual(response.status_code, 200)
#
#     def test_book_add(self):
#         user_login = get_jwt_identity()
#         response = self.app_test.post('/api/trips/add',
#                                       json={
#                                           "name": "Niedzielna wycieczka",
#                                           "user_login": user_login,
#                                           "date_start": "2020-08-07",
#                                           "date_end": "2020-08-09",
#                                           "score_sum": 24,
#                                       },
#                                       headers={'Authorization': 'Bearer ' + self.token})
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(Trip.query.count(), 1)
#
#     def test_edit_non_existing_book(self):
#         response = self.app_test.post('/api/fragments/edit/4',
#                                       json={},
#                                       headers={'Authorization': 'Bearer ' + self.token})
#         self.assertEqual(response.status_code, 409)
#
#     def test_edit_book_no_json(self):
#         response = self.app_test.post('/api/fragments/edit/1',
#                                       headers={'Authorization': 'Bearer ' + self.token})
#         self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()

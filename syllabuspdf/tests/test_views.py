from django.test import TestCase
from ..views import logger_view

class Logger_View_TestCase(TestCase):

    def test_successful_logging_request(self):
        self.session = {
            "course_id": "course_id123",
            "user_id": "user_id123"
        }
        response = logger_view(self)
        self.assertEqual(response.status_code, 200)

    def test_missing_course_id_request(self):
        self.session = {
            "user_id": "user_id123"
        }
        response = logger_view(self)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"'course_id' not found")
    
    def test_missing_user_id_request(self):
        self.session = {
            "course_id": "course_id123"
        }
        response = logger_view(self)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"'user_id' not found")

        
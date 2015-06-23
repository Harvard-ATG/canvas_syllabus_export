from django.test import TestCase
from django.test import Client

class SyllabusPDFTestCase(TestCase):
	def test_index(self):
		c = Client()
		r = c.get('/syllabuspdf/')
		self.assertEqual(r.status_code, 200) 


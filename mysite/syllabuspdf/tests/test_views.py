from django.test import TestCase
from syllabuspdf.views import index

class SyllabusPDFTestCase(TestCase):
	def test_index(self):
		r = self.client.get('/syllabuspdf/')
		self.assertEqual(r.status_code, 200)
		self.assertTemplateUsed(r, 'syllabuspdf/index.html')
		self.assertTrue('syllabus' in r.context)
		self.assertTrue('events' in r.context)
		self.assertTrue('groups' in r.context)
		self.assertTrue('form' in r.context)
		self.assertTrue('settings' in r.context)
		self.assertEqual(r.context['settings'], {'syllabus' : True, 'events' : True, 'descriptions': True, 'times': True, 'weights':True, 'hidden_field':"field"})



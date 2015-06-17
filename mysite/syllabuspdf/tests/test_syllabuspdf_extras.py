from django.test import TestCase

from syllabuspdf.templatetags.syllabuspdf_extras import convert_tz, format_date, format_time, escape_None

class SyllabusPDF_ExtrasTestCase(TestCase):
	def test_convert_tz(self):
		pass

	def test_format_date(self):
		self.assertEqual(format_date(None), "")

	def test_format_time(self):
		pass

	def test_escape_None(self):
		self.assertEqual(escape_None(None), "")
		self.assertEqual(escape_None("str"), "str")
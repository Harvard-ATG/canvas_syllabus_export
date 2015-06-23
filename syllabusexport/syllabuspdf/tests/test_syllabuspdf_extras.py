from django.test import TestCase

from syllabuspdf.templatetags.syllabuspdf_extras import convert_tz, format_date, format_time, escape_None

class SyllabusPDF_ExtrasTestCase(TestCase):
	def test_convert_tz(self):
		from datetime import datetime
		from django.utils import timezone
		from dateutil import tz
		self.assertEqual(datetime(2015,3,10,4,57,44).replace(tzinfo=tz.gettz('America/New_York')), convert_tz(datetime(2015,3,10,8,57,44)))

	def test_format_date(self):
		self.assertEqual(format_date(None), "")
		self.assertEqual(format_date("2015-03-10T22:57:44Z"), "Tue Mar 10, 2015")

	def test_format_time(self):
		self.assertEqual(format_time(None, ""), "")
		self.assertEqual(format_time("", None), "")
		self.assertEqual(format_time(None, None), "")
		self.assertEqual(format_time("2015-03-10T22:57:44Z", "2015-03-10T22:57:44Z"), "due by 06:57PM")
		self.assertEqual(format_time("2015-03-10T21:57:44Z", "2015-03-10T22:57:44Z"), "05:57PM to 06:57PM")

	def test_escape_None(self):
		self.assertEqual(escape_None(None), "")
		self.assertEqual(escape_None("str"), "str")
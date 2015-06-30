from django.test import TestCase
from syllabuspdf.apirequest import sort_events, filter_undated

class ApiRequestTestCase(TestCase):
	def test_sort_events(self):
		e1 = {'end_at': None}
		e2 = {'end_at': None}
		e3 = {'end_at':"3"}
		e4 = {'end_at':"4"}
		e5 = {'end_at':"5"}
		e6 = {'end_at': None}
		self.assertEqual(sort_events([]), [])
		self.assertEqual(sort_events([e1]), [e1])
		self.assertEqual(sort_events([e3]), [e3])
		self.assertEqual(sort_events([e4, e3, e5]), [e3, e4, e5])
		self.assertEqual(sort_events([e3, e2, e5, e1, e4]), [e2, e1, e3, e4, e5])

	def test_filter_undated(self):
		e1 = {'end_at': None}
		e2 = {'end_at': None}
		e3 = {'end_at':"3"}
		e4 = {'end_at':"4"}
		e5 = {'end_at':"5"}
		e6 = {'end_at': None}
		self.assertEqual(filter_undated([]), ([],[]))
		self.assertEqual(filter_undated([e1, e2, e3, e4, e5]), ([e3, e4, e5],[e1, e2]))
		self.assertEqual(filter_undated([e3, e4, e5, e1, e2]), ([e3, e4, e5],[e1, e2]))
		self.assertEqual(filter_undated([e1]), ([],[e1]))
		self.assertEqual(filter_undated([e3]), ([e3],[]))
		self.assertEqual(filter_undated([e3, e2, e5, e1, e4]), ([e3, e5, e4], [e2, e1]))
		self.assertEqual(filter_undated([e2, e1, e6, e4]), ([e4], [e2, e1, e6]))






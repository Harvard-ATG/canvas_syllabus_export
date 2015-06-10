# Helper functions for generation of pdf view
import requests

# Base URL
baseurl = "https://canvas.harvard.edu/api/v1/"

def fetch_syllabus(id, token):
	'''Fetches syllabus for course with given id and token from API. Returns syllabus as HTML string'''
	
	headers = {"Authorization": "Bearer " + token}
	params = {'include[]': 'syllabus_body'}
	requesturl = baseurl + "courses/" + str(id) 

	# Make request
	r = requests.get(requesturl, headers = headers, params = params)

	# Decode JSON
	syllabus = r.json()

	return syllabus['syllabus_body']


def fetch_allevents(id, token):
	'''Fetches assignments and events for course with given id and token'''

	headers = {"Authorization": "Bearer " + token}
	assignparams = {"all_events": "true", "type" : "assignment", "context_codes[]" : "course_" + str(id)}
	eventparams = {"all_events": "true", "context_codes[]" : "course_" + str(id)} 

	requesturl = baseurl + "calendar_events/"

	# Make requests
	assignr = requests.get(requesturl, headers = headers, params = assignparams)
	eventr = requests.get(requesturl, headers = headers, params = eventparams)
	
	assignments = assignr.json()
	events = eventr.json()

	# Merge lists
	allevents = assignments + events

	# Sort assignments by time
	sortedevents = sorted(allevents, key = lambda a: a['end_at'])

	return sortedevents
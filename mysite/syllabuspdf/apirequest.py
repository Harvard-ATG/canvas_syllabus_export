# Makes Canvas API requests using the Canvas Python SDK
from canvas_sdk.client import auth, base, request_context
from canvas_sdk.utils import get_all_list_data
from collections import deque

oauthtoken = "1875~6EHVRVunNzwmeaHXOm4Yji3uZOh3baRLVJU4yT6UO4NLnCRUYA0ByAx1pQi1IbGy"

baseurl = "https://canvas.harvard.edu/api"

def fetch_syllabus(id):
	'''Fetches syllabus for course with given id from API. Returns syllabus as HTML string'''
	
	# Create request context
	req_context = request_context.RequestContext(oauthtoken, baseurl)

	# Make API request
	r = base.call("GET", baseurl + "/v1/courses/" + str(id), req_context, params={'include[]': 'syllabus_body'}, auth_token=oauthtoken)

	# Decode JSON
	syllabus = r.json()

	return syllabus['syllabus_body']

def fetch_allevents(id):
	'''Fetches assignments and events for course with given id'''

	# Create request context
	req_context = request_context.RequestContext(oauthtoken, baseurl)

	# Create separate parameters for assignment event and calendar event requests
	assignparams = {"all_events": "true", "type" : "assignment", "context_codes[]" : "course_" + str(id)}
	eventparams = {"all_events": "true", "context_codes[]" : "course_" + str(id)} 

	# Make requests
	assignments = get_all_list_data(req_context, base.get, baseurl + "/v1/calendar_events", params=assignparams, auth_token=oauthtoken)
	events = get_all_list_data(req_context, base.get, baseurl + "/v1/calendar_events", params=eventparams, auth_token=oauthtoken)

	# Merge lists
	allevents = assignments + events

	# Sort assignments by time
	sortedevents = sorted(allevents, key = lambda a: a['end_at'])

	return sortedevents


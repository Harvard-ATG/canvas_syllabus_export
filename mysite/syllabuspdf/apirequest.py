# Makes Canvas API requests using the Canvas Python SDK
from canvas_sdk.client import auth, base, request_context
from canvas_sdk.utils import get_all_list_data
from collections import deque

from secure import SECURE_SETTINGS

oauthtoken = SECURE_SETTINGS.get('oauthtoken', None)

baseurl = "https://canvas.harvard.edu/api"

def fetch_syllabus(id):
	'''Fetches syllabus for course with given id from API. Returns syllabus as HTML string'''
	if oauthtoken is None:
		raise Exception("Invalid Authorization Token")

	# Create request context
	req_context = request_context.RequestContext(oauthtoken, baseurl)

	# Make API request
	r = base.call("GET", baseurl + "/v1/courses/" + str(id), req_context, params={'include[]': 'syllabus_body'}, auth_token=oauthtoken)

	# Decode JSON
	syllabus = r.json()

	return syllabus['syllabus_body']

def fetch_allevents(id):
	'''Fetches assignments and events for course with given id'''
	if oauthtoken is None:
		raise Exception("Invalid Authorization Token")

	# Create request context
	req_context = request_context.RequestContext(oauthtoken, baseurl)

	# Create separate parameters for assignment event and calendar event requests
	assignparams = {"all_events": "true", "type" : "assignment", "context_codes[]" : "course_" + str(id)}
	eventparams = {"all_events": "true", "context_codes[]" : "course_" + str(id)} 

	# Make requests, making sure to get all the data
	assignments = get_all_list_data(req_context, base.get, baseurl + "/v1/calendar_events", params=assignparams, auth_token=oauthtoken)
	events = get_all_list_data(req_context, base.get, baseurl + "/v1/calendar_events", params=eventparams, auth_token=oauthtoken)

	# Merge lists
	allevents = assignments + events

	# Sort events
	sortedevents = sort_events(allevents)

	return sortedevents

def fetch_assigngroups(id):
	'''Fetches assignment groups for course with given id'''
	if oauthtoken is None:
		raise Exception("Invalid Authorization Token")

	# Create request context
	req_context = request_context.RequestContext(oauthtoken, baseurl)

	# URL for request
	url = baseurl + "/v1/courses/" + str(id) + "/assignment_groups"

	# Make request, making sure to get all results
	groups = get_all_list_data(req_context, base.get, url, auth_token=oauthtoken)

	return groups

def sort_events(events):
	'''Sorts assignments by time and moves unsorted ones to the end'''
	return append_undated(sorted(events, key = lambda a: a['end_at']))

def append_undated(events):
	'''Moves all undated events in an event list to the end'''
	undated = filter(lambda e: e['end_at'] is None, events)
	# Create new list, filtering out undated events
	filtered = filter(lambda e: e['end_at'] is not None, events)
	# Append undated events to filtered list
	finallist = filtered + undated[::-1]
	return finallist

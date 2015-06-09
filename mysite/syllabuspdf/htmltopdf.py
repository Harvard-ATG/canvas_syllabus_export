# Helper functions for generation of pdf view
import requests

# Oauth token for testing
oauthtoken = "1875~6EHVRVunNzwmeaHXOm4Yji3uZOh3baRLVJU4yT6UO4NLnCRUYA0ByAx1pQi1IbGy"

# Sample Course ID
courseid = 2502

# Base URL
baseurl = "https://canvas.harvard.edu/api/v1/courses/"

def create_URL (id):
	'''Create URL for API request'''
	return baseurl + str(id)

def fetch_syllabus(id, token):
	'''Fetches syllabus for course with given id and token from API. Returns syllabus as HTML string'''
	
	headers = {"Authorization": "Bearer " + token}
	params = {'include[]': 'syllabus_body'}
	requesturl = create_URL(id)

	# Make request
	r = requests.get(requesturl, headers = headers, params = params)

	# Decode JSON
	syllabus = r.json()

	return syllabus['syllabus_body']

def fetch_assignments(id, token):
	'''Fetches assignments for course with given id and token'''

	headers = {"Authorization": "Bearer " + token} 
	requesturl = create_URL(id) + "/assignments"

	# Make request
	r = requests.get(requesturl, headers = headers)
	assignments = r.json()

	# Sort assignments by time
	sortedassign = sorted(assignments, key = lambda a: a['due_at'])
	
	# Format times of all assigments
	for assignment in sortedassign:
		if isinstance(assignment['due_at'], str):
			assignment['due_at'] = format_time(assignment['due_at'])

	return sortedassign
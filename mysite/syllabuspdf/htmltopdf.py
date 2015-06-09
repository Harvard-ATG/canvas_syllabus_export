# Helper functions for generation of pdf view
import requests
import datetime
from re import sub

from xhtml2pdf import pisa
from StringIO import StringIO

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

def format_time(str):
	'''Converts a time string into a more readable format'''
	
	# Clean string by stripping all non numeric characters
	cleaned = sub("[^0-9]", "", str)

	# Store formatted time
	tformatted = datetime.datetime.strptime(cleaned, "%Y%m%d%H%M%S")

	# Time string in format for display on webpage
	time = tformatted.strftime('%a %b %d, %Y')

	return time

def HTML_to_PDF(html):
	'''Converts HTML string to PDF string'''
	pdf = StringIO()
	pisaStatus = pisa.CreatePDF(StringIO(html.encode('utf-8')), pdf)
	return pdf.getvalue()

def PDF_as_string(id, token):
	'''Returns syllabus PDF as string'''
	syllabus = fetch_syllabus(id, token)
	return HTML_to_PDF(syllabus)
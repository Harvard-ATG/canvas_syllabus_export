# Given a course id and oauth token (hardcoded right now), exports syllabus as PDF
# Potential issue: pdfkit is a wrapper for wkhtmltopdf, a command line tool which has to be installed
import pdfkit
import requests

# Oauth token for testing
oauthtoken = "1875~6EHVRVunNzwmeaHXOm4Yji3uZOh3baRLVJU4yT6UO4NLnCRUYA0ByAx1pQi1IbGy"

# Sample Course ID
courseid = 2502

# Base URL
baseurl = "https://canvas.harvard.edu/api/v1/courses/"

def create_URL ():
	'''Create URL for API request'''
	return baseurl + str(courseid)

def fetch_syllabus(id, token):
	'''Fetches syllabus for course with given id and token from API. Returns syllabus as HTML string'''
	
	headers = {"Authorization": "Bearer " + token}
	params = {'include[]': 'syllabus_body'}
	requesturl = create_URL()

	# Make request
	r = requests.get(requesturl, headers = headers, params = params)

	# Parse JSON
	parsedJSON = r.json()

	return parsedJSON[u'syllabus_body']

def HTML_to_PDF(html):
	'''Converts syllabus in HTML form to PDF'''
	return pdfkit.from_string(html, False)

def PDF_as_string(id, token):
	'''Returns syllabus PDF as string'''
	syllabus = fetch_syllabus(id, token)
	return HTML_to_PDF(syllabus)
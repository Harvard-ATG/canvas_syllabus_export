import datetime
from django import template
from django.template.defaultfilters import stringfilter
from re import sub

register = template.Library()

@register.filter
def format_time(str):
	'''Converts a time string into a more readable format'''
	
	# Clean string by stripping all non numeric characters
	cleaned = sub("[^0-9]", "", str)

	# Store formatted time
	tformatted = datetime.datetime.strptime(cleaned, "%Y%m%d%H%M%S")

	# Time string in format for display on webpage
	time = tformatted.strftime('%a %b %d, %Y')

	return time
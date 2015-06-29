from datetime import datetime
from dateutil import tz
from django import template
from django.template.defaultfilters import stringfilter
from re import sub

register = template.Library()

def convert_tz(datetimeobj):
	'''Converts a datetimeobj from UTC to the local timezone'''
	from_zone = tz.tzutc()
	to_zone = tz.gettz('America/New_York')
	# Tell datetime object it's in UTC
	utc = datetimeobj.replace(tzinfo=from_zone)
	# Convert to local time
	local = utc.astimezone(to_zone)

	return local

@register.filter
def format_date(str):
	'''Converts a date string into a more readable format'''	
	# Check for None case
	if str is None:
		return ""

	# Clean string by stripping all non numeric characters
	cleaned = sub("[^0-9]", "", str)

	# Store formatted date as datetimeobject and convert timezone
	dformatted = convert_tz(datetime.strptime(cleaned, "%Y%m%d%H%M%S"))

	# Date string in format for display on webpage
	date = dformatted.strftime('%a %b %d, %Y')

	return date

@register.simple_tag
def format_time(startat, endat, type):
	'''Formats time for events, handling assignment events and calendar events separately'''
	# Check for None
	if (startat is None) or (endat is None):
		return ""

	# Clean strings, cutting out last six characters
	cleanedstart = sub("[^0-9]", "", startat[0:20])
	cleanedend = sub("[^0-9]", "", endat[0:20])

	if type == 'assignment':
		tformatted = convert_tz(datetime.strptime(cleanedstart, "%Y%m%d%H%M%S"))
		time = tformatted.strftime("%I:%M%p")
		return "due by " + time

	# Else calendar event
	else:
		sformatted = convert_tz(datetime.strptime(cleanedstart, "%Y%m%d%H%M%S"))
		eformatted = convert_tz(datetime.strptime(cleanedend, "%Y%m%d%H%M%S"))
		start = sformatted.strftime("%I:%M%p")
		end = eformatted.strftime("%I:%M%p")
		if start != end:
			return start + " to " + end
		else:
			return start

@register.filter
def escape_None(str):
	'''Substitutes an empty string when the event description is None'''
	if str is None:
		return ''
	return str
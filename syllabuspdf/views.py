from django.shortcuts import render
from django.http import HttpResponse
from apirequest import fetch_syllabus, fetch_allevents, fetch_assigngroups
from django.http import Http404
from django.conf import settings

from forms import SettingsForm

import logging

logger = logging.getLogger(__name__)

def index(request):
	# Get course id from session
	try:
		courseid = request.session['LTI_LAUNCH']['custom_canvas_course_id']
	except:
		logger.error("Missing custom_canvas_course_id in LTI launch")
		raise Http404("Course ID not found")

	# Get content via API calls
	syllabus = fetch_syllabus(courseid)
	(dated, undated) = fetch_allevents(courseid)
	groups = fetch_assigngroups(courseid)

	# Check for initial load of page through presence of hidden field
	if 'hidden_field' in request.GET:
		form = SettingsForm(request.GET)
		if form.is_valid():
			form_settings = form.cleaned_data
	else:
		form = SettingsForm()
		form_settings = {
			'syllabus':True,
			'dated_events':True,
			'undated_events':False,
			'descriptions':False,
			'times':True,
			'weights':False,
			'hidden_field':"viewed"
		}

	# Populate events array based on toggled options
	events = []
	if form_settings['dated_events']:
		events += dated
	if form_settings['undated_events']:
		events += undated

	context = {
		'ga_tracking_id': settings.GA_TRACKING_ID,
		'syllabus': syllabus, 
		'events': events, 
		'groups': groups, 
		'form': form, 
		'settings': form_settings
	}
	return render(request,'syllabuspdf/index.html', context)
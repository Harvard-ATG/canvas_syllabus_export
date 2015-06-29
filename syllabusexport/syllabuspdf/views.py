from django.shortcuts import render
from django.http import HttpResponse
from apirequest import fetch_syllabus, fetch_allevents, fetch_assigngroups

from forms import SettingsForm

def index(request):
	# Get course id from session
	try:
		courseid = request.session['LTI_LAUNCH']['custom_canvas_course_id']
	except:
		return HttpResponse("Course ID not found")

	# Get content via API calls
	syllabus = fetch_syllabus(courseid)
	(dated, undated) = fetch_allevents(courseid)
	groups = fetch_assigngroups(courseid)

	# Check for initial load of page through presence of hidden field
	if 'hidden_field' in request.GET:
		form = SettingsForm(request.GET)
		if form.is_valid():
			settings = form.cleaned_data
	else:
		form = SettingsForm()
		settings = {
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
	if settings['dated_events']:
		events += dated
	if settings['undated_events']:
		events += undated

	context = {'syllabus': syllabus, 'events': events, 'groups': groups, 'form': form, 'settings': settings}
	return render(request,'syllabuspdf/index.html', context)
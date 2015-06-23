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
	syllabus = fetch_syllabus(courseid)
	events = fetch_allevents(courseid)
	groups = fetch_assigngroups(courseid)

	if 'hidden_field' in request.GET:
		form = SettingsForm(request.GET)
		if form.is_valid():
			settings = form.cleaned_data
	else:
		form = SettingsForm()
		settings = {'syllabus' : True, 'events' : True, 'descriptions': True, 'times': True, 'weights':True, 'hidden_field':"field"}

	context = {'syllabus': syllabus, 'events': events, 'groups': groups, 'form': form, 'settings': settings}
	return render(request,'syllabuspdf/index.html', context)
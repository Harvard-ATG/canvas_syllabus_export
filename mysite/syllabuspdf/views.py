from django.shortcuts import render
from django.http import HttpResponse
from apirequest import fetch_syllabus, fetch_allevents, fetch_assigngroups

from xhtml2pdf import pisa
from StringIO import StringIO

from django_auth_lti.middleware import LTIAuthMiddleware

from forms import SettingsForm

courseid = 1876

def index(request):
	# Instantiate LTIAuth middleware and process request
	mw = LTIAuthMiddleware()
	mw.process_request(request)
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

def pdf_view(request):
	# Get fully rendered HTML for page from index's HttpResponse object
	responseobj = index(request)
	renderedHTML = responseobj.content

	# Buffer for storing PDF string
	pdf = StringIO()

	# Set encoding to unicode
	htmlu = unicode(renderedHTML, 'utf-8')

	pisaStatus = pisa.CreatePDF(StringIO(htmlu.encode('UTF-8')), pdf)
	if not pisaStatus.err:
		return HttpResponse(pdf.getvalue(), content_type='application/pdf')
	return HttpResponse("Error: Unsupported syllabus content")

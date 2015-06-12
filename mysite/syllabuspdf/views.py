from django.shortcuts import render
from django.http import HttpResponse
from apirequest import fetch_syllabus, fetch_allevents, fetch_assigngroups

from xhtml2pdf import pisa
from StringIO import StringIO

def index(request):
	syllabus = fetch_syllabus(1876)
	events = fetch_allevents(1876)
	groups = fetch_assigngroups(1876)
	context = {'syllabus': syllabus, 'events': events, 'groups': groups}
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
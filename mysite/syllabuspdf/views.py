from django.shortcuts import render
from django.http import HttpResponse
from apirequest import fetch_syllabus, fetch_allevents

from easy_pdf.views import PDFTemplateView

def index(request):
	syllabus = fetch_syllabus(775)
	events = fetch_allevents(775)
	context = {'syllabus': syllabus, 'events': events}
	return render(request,'syllabuspdf/index.html', context)

class SyllabusPDFView(PDFTemplateView):
    template_name = "syllabuspdf/pdf.html"

    def get_context_data(self, **kwargs):
        return super(SyllabusPDFView, self).get_context_data(
            pagesize="A4",
            title="Syllabus",
            syllabus = fetch_syllabus(775),
			events = fetch_allevents(775),
            **kwargs
        )


 

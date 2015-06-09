from django.shortcuts import render
from django.http import HttpResponse
from htmltopdf import fetch_syllabus, fetch_assignments

from easy_pdf.views import PDFTemplateView

def index(request):
	syllabus = fetch_syllabus(775, "1875~6EHVRVunNzwmeaHXOm4Yji3uZOh3baRLVJU4yT6UO4NLnCRUYA0ByAx1pQi1IbGy")
	assignments = fetch_assignments(775, "1875~6EHVRVunNzwmeaHXOm4Yji3uZOh3baRLVJU4yT6UO4NLnCRUYA0ByAx1pQi1IbGy")
	context = {'syllabus': syllabus, 'assignments': assignments}
	return render(request,'syllabuspdf/index.html', context)

class SyllabusPDFView(PDFTemplateView):
    template_name = "syllabuspdf/pdf.html"

    def get_context_data(self, **kwargs):
        return super(SyllabusPDFView, self).get_context_data(
            pagesize="A4",
            title="Syllabus",
            syllabus = fetch_syllabus(775, "1875~6EHVRVunNzwmeaHXOm4Yji3uZOh3baRLVJU4yT6UO4NLnCRUYA0ByAx1pQi1IbGy"),
			assignments = fetch_assignments(775, "1875~6EHVRVunNzwmeaHXOm4Yji3uZOh3baRLVJU4yT6UO4NLnCRUYA0ByAx1pQi1IbGy"),
            **kwargs
        )


 

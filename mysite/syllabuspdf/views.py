from django.shortcuts import render
from django.http import HttpResponse
import htmltopdf

def index(request):
	syllabus = htmltopdf.fetch_syllabus(2502, "1875~6EHVRVunNzwmeaHXOm4Yji3uZOh3baRLVJU4yT6UO4NLnCRUYA0ByAx1pQi1IbGy")
	context = {'syllabus': syllabus}
	return render(request,'syllabuspdf/index.html', context)

def pdf_view(request):
	pdf = htmltopdf.PDF_as_string(2502, "1875~6EHVRVunNzwmeaHXOm4Yji3uZOh3baRLVJU4yT6UO4NLnCRUYA0ByAx1pQi1IbGy")
	return HttpResponse(pdf, content_type='application/pdf')
 

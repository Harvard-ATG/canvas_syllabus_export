from django.shortcuts import render
from django.http import HttpResponse
import htmltopdf

def index(request):
	return HttpResponse(htmltopdf.PDF_as_string(), content_type='application/pdf')

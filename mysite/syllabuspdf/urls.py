from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^syllabus.pdf$', views.pdf_view, name='pdf')
]
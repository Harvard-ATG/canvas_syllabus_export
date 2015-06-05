from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'pdf_view/$', views.pdf_view, name='pdf_view')
]
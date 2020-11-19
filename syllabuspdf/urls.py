from django.urls import path
from . import views
from lti_provider import views as lti_views

app_name = 'syllabuspdf'
urlpatterns = [
    path('lti/launch/', views.process_lti_launch_request_view, name='process_lti_launch_request'),
    path('lti/config/', lti_views.LTIConfigView.as_view(), name='get_lti_xml'),
	path('index', views.index, name='index'),
]
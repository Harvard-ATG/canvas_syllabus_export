from __future__ import absolute_import
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.conf import settings
from lti_provider.lti import LTI
from pylti.common import LTIException
from urllib.parse import parse_qs, urlparse, urlencode, urlunparse
from .apirequest import fetch_syllabus, fetch_allevents, fetch_assigngroups
from .forms import SettingsForm
import logging


logger = logging.getLogger(__name__)


@csrf_exempt
def process_lti_launch_request_view(request):
    '''
    Processes the lti launch request and redirects to the index view
    '''
    #True if this is a typical lti launch. False if not.
    is_basic_lti_launch = request.method == 'POST' and request.POST.get(
        'lti_message_type') == 'basic-lti-launch-request'

    lti = LTI(request_type="any", role_type="any")
    try:
        request_is_valid = lti.verify(request)
    except LTIException:  # oauth session may have timed out or the LTI key/secret pair may be wrong
        return HttpResponseBadRequest('<p>Something went wrong. Reload the page, or contact atg@fas.harvard.edu.<p>')

    if is_basic_lti_launch and request_is_valid:
        # Store the custom_canvas_course_id in the request's session attribute.
        request.session['course_id'] = request.POST.get('custom_canvas_course_id')
        return redirect('syllabuspdf:index')
    else:
        raise PermissionDenied


@csrf_exempt
def index(request):
    # Get course id from session
    try:
        logger.debug('Obtaining course id from session ...')
        courseid = request.session['course_id']
        logger.debug('Course id is %s' % (courseid))
    except:
        raise Http404('Course ID not found')

    # Get content via API calls
    syllabus = fetch_syllabus(courseid)
    (dated, undated) = fetch_allevents(courseid)
    groups = fetch_assigngroups(courseid)

    # Check for initial load of page through presence of hidden field
    if 'hidden_field' in request.GET:
        form = SettingsForm(request.GET)
        if form.is_valid():
            form_settings = form.cleaned_data
    else:
        form = SettingsForm()
        form_settings = {
            'syllabus': True,
            'dated_events': True,
            'undated_events': False,
            'descriptions': False,
            'times': True,
            'weights': False,
            'hidden_field': "viewed"
        }

    # Populate events array based on toggled options
    events = []
    if form_settings['dated_events']:
        events += dated
    if form_settings['undated_events']:
        events += undated

    context = {
        'ga_tracking_id': settings.GA_TRACKING_ID,
        'syllabus': syllabus,
        'events': events,
        'groups': groups,
        'form': form,
        'settings': form_settings
    }
    return render(request, 'syllabuspdf/index.html', context)

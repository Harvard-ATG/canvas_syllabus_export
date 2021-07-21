from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from lti_provider.lti import LTI
from pylti.common import LTIException
from canvas_sdk.exceptions import (CanvasAPIError, InvalidOAuthTokenError)

from .apirequest import fetch_syllabus, fetch_allevents, fetch_assigngroups
from .forms import SettingsForm

import logging


logger = logging.getLogger('syllabuspdf')


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
        logger.exception("LTI launch failed")
        return HttpResponseBadRequest('<p>LTI launch failed. Please contact atg@fas.harvard.edu for assistance.<p>')

    if is_basic_lti_launch and request_is_valid:
        # Store the custom_canvas_course_id in the request's session attribute.
        course_id = request.POST.get('custom_canvas_course_id')
        user_id = request.POST.get('user_id')
        logger.info(f"LTI launch valid: course_id={course_id} user_id={user_id}")
        request.session['user_id'] = user_id
        request.session['course_id'] = course_id
        request.session.modified = True
        return redirect('syllabuspdf:index', permanent=False)
    else:
        logger.info(f"LTI launch invalid: is_basic_lti_launch={is_basic_lti_launch} request_is_valid={request_is_valid}")
        raise PermissionDenied


@csrf_exempt
def index(request):
    # Get course id from session
    try:
        course_id = request.session['course_id']
        user_id = request.session['user_id']
        logger.info(f"Syllabus index: course_id={course_id} user_id={user_id}")
    except:
        logger.error("Syllabus index: canvas course ID not found in session")
        raise Http404('Course ID not found')

    # Get content via API calls
    try:
        syllabus = fetch_syllabus(course_id)
        (dated, undated) = fetch_allevents(course_id)
        groups = fetch_assigngroups(course_id)
        logger.info(f"Syllabus index: Canvas API data loaded successfully: course_id={course_id} user_id={user_id}")
    except (CanvasAPIError, InvalidOAuthTokenError):
        logger.exception(f"Syllabus index: Canvas API error: course_id={course_id} user_id={user_id}")
        return HttpResponseServerError(f"Error: failed to load syllabus and assignment data from Canvas")

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

from __future__ import absolute_import
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.conf import settings
from lti_provider.lti import LTI
from pylti.common import LTIException
from lti import ToolConfig
from urllib.parse import parse_qs, urlparse, urlencode, urlunparse
from .apirequest import fetch_syllabus, fetch_allevents, fetch_assigngroups
from .forms import SettingsForm
import logging


logger = logging.getLogger(__name__)

LTI_SETUP = settings.LTI_SETUP

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


class LTIToolConfigView(View):
    LAUNCH_URL = LTI_SETUP.get('LAUNCH_URL', 'syllabuspdf:process_lti_launch_request')
    """
    Outputs LTI configuration XML for Canvas as specified in the IMS Global Common Cartridge Profile.
    The XML produced by this view can either be copy-pasted into the Canvas tool
    settings, or exposed as an endpoint to Canvas by linking to this view.
    """
    def get_launch_url(self, request):
        '''
        Returns the launch URL for the LTI tool. When a secure request is made,
        a secure launch URL will be supplied.
        '''
        if request.is_secure():
            host = 'https://' + request.get_host()
        else:
            host = 'http://' + request.get_host()
        url = host + reverse(self.LAUNCH_URL)
        return url;

    def set_ext_params(self, lti_tool_config):
        '''
        Sets extension parameters on the ToolConfig() instance.
        This includes vendor-specific things like the course_navigation
        and privacy level.
        EXAMPLE_EXT_PARAMS = {
            "canvas.instructure.com": {
                "privacy_level": "public",
                "course_navigation": {
                    "enabled": "true",
                    "default": "disabled",
                    "text": "MY tool (localhost)",
                }
            }
        }
        '''
        EXT_PARAMS = LTI_SETUP.get("EXTENSION_PARAMETERS", {})
        for ext_key in EXT_PARAMS:
            for ext_param in EXT_PARAMS[ext_key]:
                ext_value = EXT_PARAMS[ext_key][ext_param]
                lti_tool_config.set_ext_param(ext_key, ext_param, ext_value)

    def get_tool_config(self, request):
        '''
        Returns an instance of ToolConfig().
        '''
        launch_url = self.get_launch_url(request)
        return ToolConfig(
            title=LTI_SETUP['TOOL_TITLE'],
            description=LTI_SETUP['TOOL_DESCRIPTION'],
            launch_url=launch_url,
            secure_launch_url=launch_url,
        )

    def get(self, request, *args, **kwargs):
        '''
        Returns the LTI tool configuration as XML.
        '''
        lti_tool_config = self.get_tool_config(request)
        self.set_ext_params(lti_tool_config)
        return HttpResponse(lti_tool_config.to_xml(), content_type='text/xml', status=200)
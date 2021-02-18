"""
Django settings for canvas_syllabus_export project.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from .secure import SECURE_SETTINGS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Base URL for Canvas instance
BASE_URL = SECURE_SETTINGS.get('base_url', "https://canvas.harvard.edu/api")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECURE_SETTINGS.get('secret_key')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lti_provider',
    'syllabuspdf',   
]

# Oauth token for making calls to Canvas API
OAUTH_TOKEN = SECURE_SETTINGS.get("oauthtoken", None)

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'lti_provider.auth.LTIBackend',
)

ROOT_URLCONF = 'canvas_syllabus_export.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'canvas_syllabus_export.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

REDIS_HOST = SECURE_SETTINGS.get('redis_host', '127.0.0.1')
REDIS_PORT = SECURE_SETTINGS.get('redis_port', 6379)

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': "%s:%s" % (REDIS_HOST, REDIS_PORT),
        'KEY_PREFIX': 'canvas_syllabus_export', # Provide a unique value for shared cache
        'TIMEOUT': SECURE_SETTINGS.get('cache_timeout_in_secs', 60 * 20),
    },
}

# Add LTI configuration settings
LTI_TOOL_CONFIGURATION = {
    'title': 'Syllabus Export',
    'description': 'Exports course syllabus as html, with additional option of generating a PDF',
    'launch_url': 'lti/launch/',
    'landing_url': '/',
    'privacy_level': 'Public',
    'course_navigation': {
        "default": "enabled",
        "enabled": "true",
        "visibility": "admins",
        "text": "Syllabus Export",
    },
}

PYLTI_CONFIG = {
    'consumers': {
        SECURE_SETTINGS.get('consumer_key', 'myconsumerkey'): {
            'secret': SECURE_SETTINGS.get('lti_secret', 'myltisecret')
        }
    }
}

# Google Analytics 
GA_TRACKING_ID = SECURE_SETTINGS.get('ga_tracking_id', None)


X_FRAME_OPTIONS = SECURE_SETTINGS.get('X_FRAME_OPTIONS', 'ALLOW-FROM https://canvas.harvard.edu/')

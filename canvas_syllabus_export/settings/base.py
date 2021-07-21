"""
Django settings for canvas_syllabus_export project.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
from .secure import SECURE_SETTINGS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Base URL for Canvas instance
BASE_URL = SECURE_SETTINGS.get('base_url', "https://canvas.harvard.edu/api")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECURE_SETTINGS.get('secret_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = SECURE_SETTINGS.get('enable_debug', False)

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


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': SECURE_SETTINGS.get('db_default_name', 'canvas_syllabus_export'),
        'USER': SECURE_SETTINGS.get('db_default_user', 'canvas_syllabus_export'),
        'PASSWORD': SECURE_SETTINGS.get('db_default_password'),
        'HOST': SECURE_SETTINGS.get('db_default_host', '127.0.0.1'),
        'PORT': SECURE_SETTINGS.get('db_default_port', 5432),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'http_static'))
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'syllabuspdf', 'static'),
)


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

# Logging settings
_DEFAULT_LOG_LEVEL = SECURE_SETTINGS.get('log_level', 'DEBUG')
_LOG_ROOT = SECURE_SETTINGS.get('log_root', '')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s\t%(asctime)s.%(msecs)03dZ\t%(name)s:%(lineno)s\t%(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s\t%(name)s:%(lineno)s\t%(message)s',
        },
    },
    'handlers': {
        # By default, log to a file
        'default': {
            'class': 'logging.handlers.WatchedFileHandler',
            'level': _DEFAULT_LOG_LEVEL,
            'formatter': 'verbose',
            'filename': os.path.join(_LOG_ROOT, 'django-canvas_syllabus_export.log'),
        },
        'console': {
            'level' : 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'simple'
        },
    },
    'loggers': {
        # Root logger
        '': {
            'level': 'WARNING',
            'handlers': ['console', 'default'],
        },
        # Add app or module specific loggers here.
        'django': {
            'handlers': ['console', 'default'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.db': {
            'handlers': ['console', 'default'],
            'level': 'INFO', # Set to DEBUG to see SQL output
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'default'],
            'level': 'INFO',
            'propagate': False,
        },
        'pylti.common': {
            'handlers': ['console', 'default'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'syllabuspdf': {
            'handlers': ['console', 'default'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

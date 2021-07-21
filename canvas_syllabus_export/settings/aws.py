from .base import *

ALLOWED_HOSTS = ['.tlt.harvard.edu']

# AWS SSL settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

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
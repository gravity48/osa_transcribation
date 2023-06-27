import os

from corsheaders.defaults import default_headers

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
}

CORS_ALLOW_HEADERS = default_headers + ('Access-Control-Allow-Origin',)

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = os.environ['DJANGO_CORS_ALLOWED_ORIGINS'].split(';')


SPECTACULAR_SETTINGS = {
    'TITLE': 'Transcribing Server API',
    'DESCRIPTION': 'Backend for transcribing service',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

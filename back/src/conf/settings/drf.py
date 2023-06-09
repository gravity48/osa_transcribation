import os

from corsheaders.defaults import default_headers

REST_FRAMEWORK = {
    'NON_FIELD_ERRORS_KEY': 'all',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',

    ),
    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework.renderers.JSONRenderer',
    # ),
    # 'DEFAULT_PARSER_CLASSES': (
    #     'rest_framework.parsers.JSONParser',
    #     'rest_framework.parsers.MultiPartParser',
    #     'rest_framework.parsers.FileUploadParser',
    #     'rest_framework.parsers.FormParser',
    # ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    # 'EXCEPTION_HANDLER': 'api.utils.custom_exception_handler',
}

CORS_ALLOW_HEADERS = default_headers + (
    'Access-Control-Allow-Origin',
)

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = os.environ['DJANGO_CORS_ALLOWED_ORIGINS'].split(';')
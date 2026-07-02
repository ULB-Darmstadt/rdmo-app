from rdmo.core.settings import REST_FRAMEWORK

'''
Debug mode, don't use this in production
'''

DEBUG = True

INSTALLED_APPS = ['dev_tools'] + INSTALLED_APPS


"""
DRF and Debug Toolbar
"""

INSTALLED_APPS += [
    'drf_spectacular', 'drf_spectacular_sidecar'
]

REST_FRAMEWORK.update(
    {
        'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
        'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
        'DEFAULT_VERSION': 'v1',
        'ALLOWED_VERSIONS': ('v1',),
    }
)

# first install with: pip install django-debug-toolbar django-model-info
INSTALLED_APPS += [
    "debug_toolbar",
    "django_model_info.apps.DjangoModelInfoConfig",
]
MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE
INTERNAL_IPS = ["127.0.0.1"]


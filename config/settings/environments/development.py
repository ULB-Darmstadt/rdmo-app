import sys
import importlib.util
from pathlib import Path



'''
Debug mode, don't use this in production
'''

DEBUG = True

'''
Authentication methods ordered by usage: shibboleth, django-allauth, ldap
'''
# from .auth import get_auth_config
# get_auth_config(INSTALLED_APPS, AUTHENTICATION_BACKENDS, MIDDLEWARE)

# Verify contents of the module:
# print(dir(module))

'''
Extra debug settings
'''
# enable browsable API in DEBUG mode
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
)

'''
Extra debug toolbar settings
'''
DEBUG_TOOLBAR = get_env_variable('DEBUG_TOOLBAR', default=False, var_type='bool')

# enable debug toolbar
if DEBUG_TOOLBAR:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
    INTERNAL_IPS = ['127.0.0.1']

'''
Extra modules
'''

if ENABLE_CATALOGS_TABLE_APP:
    INSTALLED_APPS += ['django_tables2', 'catalogs_table_app']

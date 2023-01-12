from .base import * 

'''
Debug mode, don't use this in production
'''

DEBUG = True

'''
Authentication methods ordered by usage: shibboleth, django-allauth, ldap
'''

'''
Shibboleth, see also:
http://rdmo.readthedocs.io/en/latest/configuration/authentication/shibboleth.html
'''

USE_SHIBBOLETH = get_env_variable('USE_SHIBBOLETH', default=False, var_type='bool')

if USE_SHIBBOLETH:
    print('\n===-- SHIBBOLETH is enabled --===\n')
    SHIBBOLETH = True
    
    PROFILE_UPDATE = False
    
    INSTALLED_APPS += ['shibboleth']
    
    SHIBBOLETH_ATTRIBUTE_MAP = {
        'uid': (True, 'username'),
        'givenName': (True, 'first_name'),
        'sn': (True, 'last_name'),
        'mail': (True, 'email'),
    }
    
    AUTHENTICATION_BACKENDS.append('shibboleth.backends.ShibbolethRemoteUserBackend')
    
    MIDDLEWARE.insert(
        MIDDLEWARE.index('django.contrib.auth.middleware.AuthenticationMiddleware') + 1,
        'shibboleth.middleware.ShibbolethRemoteUserMiddleware'
    )
    
    LOGIN_URL = '/Shibboleth.sso/Login?target=/projects'
    LOGOUT_URL = '/Shibboleth.sso/Logout'

'''
Allauth configuration, see also:
http://rdmo.readthedocs.io/en/latest/configuration/authentication/allauth.html

Keycloak via allauth:
https://django-allauth.readthedocs.io/en/latest/providers.html#keycloak
'''

USE_ALLAUTH = get_env_variable('USE_ALLAUTH', default=False, var_type='bool')

USE_KEYCLOAK = get_env_variable('USE_KEYCLOAK', default=False, var_type='bool')

if USE_ALLAUTH or USE_KEYCLOAK:
    print('\n===-- AllAuth is enabled --===\n')
    
    ACCOUNT = True
    ACCOUNT_SIGNUP = False
    SOCIALACCOUNT = True
    SOCIALACCOUNT_SIGNUP = True
    SOCIALACCOUNT_AUTO_SIGNUP = True

    INSTALLED_APPS += [
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        # 'allauth.socialaccount.providers.facebook',
        # 'allauth.socialaccount.providers.github',
        # 'allauth.socialaccount.providers.google',
        # 'allauth.socialaccount.providers.orcid',
        # 'allauth.socialaccount.providers.twitter',
        
    ]
    AUTHENTICATION_BACKENDS.append('allauth.account.auth_backends.AuthenticationBackend')

if USE_KEYCLOAK:
    SOCIALACCOUNT_PROVIDERS = {
        'keycloak': {
            'KEYCLOAK_URL': get_env_variable('KEYCLOAK_SERVER_URL'),
            'KEYCLOAK_REALM': get_env_variable('KEYCLOAK_REALM')
        },
    }
    INSTALLED_APPS += ['allauth.socialaccount.providers.keycloak',]

'''
Extra debug settings
'''
DATA_UPLOAD_MAX_NUMBER_FIELDS = int(get_env_variable('DATA_UPLOAD_MAX_NUMBER_FIELDS', 1000))
# enable browsable API in DEBUG mode
if DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )

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
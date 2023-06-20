
'''
Shibboleth, see also:
http://rdmo.readthedocs.io/en/latest/configuration/authentication/shibboleth.html
'''
from os import environ

AUTH_USE_SHIBBOLETH = environ('AUTH_USE_SHIBBOLETH', False)

if AUTH_USE_SHIBBOLETH:
    print('\n===-- SHIBBOLETH is enabled --===\n')
    SHIBBOLETH = True

    PROFILE_UPDATE = False
    PROFILE_DELETE = False

    INSTALLED_APPS += ['shibboleth']

    SHIBBOLETH_UNQUOTE_ATTRIBUTES = True

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

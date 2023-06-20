
'''
Authentication methods ordered by usage: shibboleth, django-allauth, ldap
'''
from os import environ

'''
Allauth configuration, see also:
http://rdmo.readthedocs.io/en/latest/configuration/authentication/allauth.html

Keycloak via allauth:
https://django-allauth.readthedocs.io/en/latest/providers.html#keycloak
'''

AUTH_USE_KEYCLOAK = environ.get('AUTH_USE_KEYCLOAK', False)
AUTH_USE_NFDI_AAI = environ.get('AUTH_USE_NFDI_AAI', False)


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

if AUTH_USE_KEYCLOAK:
    print('\n===-- AllAuth/Keycloak is enabled --===\n')
    SOCIALACCOUNT_PROVIDERS = {
        'keycloak': {
            'KEYCLOAK_URL': get_env_variable('KEYCLOAK_SERVER_URL'),
            'KEYCLOAK_REALM': get_env_variable('KEYCLOAK_REALM')
        },
    }
    INSTALLED_APPS += ['allauth.socialaccount.providers.keycloak', ]


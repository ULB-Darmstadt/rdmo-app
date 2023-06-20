import sys
import importlib.util
from pathlib import Path
from os import environ

from django.core.exceptions import ImproperlyConfigured

from ...tools import get_env_variable


def get_auth_config():
    AUTH_USE_ALLAUTH = get_env_variable('AUTH_USE_ALLAUTH', default=False, var_type='bool')
    AUTH_USE_KEYCLOAK = get_env_variable('AUTH_USE_KEYCLOAK', default=False, var_type='bool')
    AUTH_USE_NFDI_AAI = get_env_variable('AUTH_USE_NFDI_AAI', default=False, var_type='bool')

    AUTH_USE_SHIBBOLETH = get_env_variable('AUTH_USE_SHIBBOLETH', default=False, var_type='bool')

    AUTH_USE_LDAP = get_env_variable('AUTH_USE_LDAP', default=False, var_type='bool')
    if AUTH_USE_ALLAUTH:
        module_name = 'allauth'

    if AUTH_USE_SHIBBOLETH:
        if AUTH_USE_ALLAUTH:
            raise ImproperlyConfigured('Shibboleth and Allauth are mutually exclusive.')
        module_name = 'shibboleth'

    if AUTH_USE_LDAP:
        module_name = 'ldap'

    return module_name
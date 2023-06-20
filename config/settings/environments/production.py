from .base import *

DEBUG = False
'''

Authentication Methods from config/settings/auth folder:
    * allauth
        AUTH_USE_ALLAUTH, AUTH_USE_KEYCLOAK or AUTH_USE_NFDI_AAI
    * shibboleth (currently mutually exclusive)
        AUTH_USE_SHIBBOLETH
    * ldap
        AUTH_USE_LDAP
The desired settings below
'''





'''
EXPORT_REFERENCE_DOCX
'''

EXPORT_REFERENCE_DOCX = get_env_variable('EXPORT_REFERENCE_DOCX', default='', var_type='path')

'''
Extra modules
'''

if ENABLE_CATALOGS_TABLE_APP:
    INSTALLED_APPS += ['django_tables2', 'catalogs_table_app']

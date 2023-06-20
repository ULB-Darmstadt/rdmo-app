from pathlib import Path

from .tools import get_env_variable, check_env_file_exists

from rdmo.core.utils import sanitize_url

from dotenv import load_dotenv

'''
Import default settings from rdmo.core
'''

from rdmo.core.settings import *

'''
Multisite settings with SITE_ID and a common DB .env file in MULTISITE_DB_ENV_FILE 
'''

MULTISITE = get_env_variable('MULTISITE', default=True, var_type='bool')
SITE_ID = get_env_variable('SITE_ID', var_type='int')
USE_MULTISITE_DB = get_env_variable('USE_MULTISITE_DB', default=True, var_type='bool')
if (MULTISITE or SITE_ID) and USE_MULTISITE_DB:
    MULTISITE_DB_ENV_FILE = get_env_variable('MULTISITE_DB_ENV_FILE', var_type='path')
    check_env_file_exists(MULTISITE_DB_ENV_FILE)
    load_dotenv(MULTISITE_DB_ENV_FILE, override=True)

'''
The default list of URLs und which this application available
'''

ALLOWED_HOSTS_DEFAULT = ['localhost', 'ip6-localhost', '127.0.0.1', '[::1]']
ALLOWED_HOSTS_ENV = get_env_variable('ALLOWED_HOSTS').split(', ')
ALLOWED_HOSTS = ALLOWED_HOSTS_DEFAULT + ALLOWED_HOSTS_ENV if any(ALLOWED_HOSTS_ENV) else ALLOWED_HOSTS_DEFAULT

'''
Language code and time zone
'''

LANGUAGE_CODE = 'de-de'
TIME_ZONE = 'Europe/Berlin'

'''
The root url of your application, only needed when its not '/'
'''

BASE_URL = get_env_variable('BASE_URL', default='')

# prepend the local.BASE_URL to the different URL settings
if BASE_URL:
    LOGIN_URL = sanitize_url(BASE_URL + LOGIN_URL)
    LOGIN_REDIRECT_URL = sanitize_url(BASE_URL + LOGIN_REDIRECT_URL)
    LOGOUT_URL = sanitize_url(BASE_URL + LOGOUT_URL)
    ACCOUNT_LOGOUT_REDIRECT_URL = sanitize_url(BASE_URL)
    MEDIA_URL = sanitize_url(BASE_URL + MEDIA_URL)
    STATIC_URL = sanitize_url(BASE_URL + STATIC_URL)

    CSRF_COOKIE_PATH = sanitize_url(BASE_URL + '/')
    LANGUAGE_COOKIE_PATH = sanitize_url(BASE_URL + '/')
    SESSION_COOKIE_PATH = sanitize_url(BASE_URL + '/')

'''
A secret key for a particular Django installation. This is used to provide
cryptographic signing, and should be set to a unique, unpredictable value.
'''

SECRET_KEY = get_env_variable('SECRET_KEY')

'''
RDMO default URI prefix
https://rdmo.readthedocs.io/en/latest/management/index.html
e.g. 'https://rdmo.uni-abc.de/terms/'
'''

DEFAULT_URI_PREFIX = get_env_variable('DEFAULT_URI_PREFIX')

'''
Locale translations paths
'''

LOCALE_PATHS = (
    BASE_DIR / 'locale/',
    BASE_DIR / 'theme/templates/locale/',
    BASE_DIR / 'accounts/templates/locale/',
)

'''
The database connection to be used, see also:
http://rdmo.readthedocs.io/en/latest/configuration/databases.html
'''

DATABASES = {
    'default': {
        'ENGINE': get_env_variable('DB_ENGINE'),
        'NAME': get_env_variable('DB_NAME'),
        'USER': get_env_variable('DB_USER'),
        'PASSWORD': get_env_variable('DB_PASSWORD'),
        'HOST': get_env_variable('DB_HOST'),
        'PORT': get_env_variable('DB_PORT'),
    }
}

'''
E-Mail configuration, see also:
http://rdmo.readthedocs.io/en/latest/configuration/email.html
'''

EMAIL_BACKEND = get_env_variable('EMAIL_BACKEND', 
                                default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = get_env_variable('EMAIL_HOST', default='localhost')
EMAIL_PORT = get_env_variable('EMAIL_PORT', default='25')

EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = get_env_variable('EMAIL_USE_TLS', 
                                default=False, var_type='bool')
EMAIL_USE_TLS = get_env_variable('EMAIL_USE_SSL', 
                                default=False, var_type='bool')
DEFAULT_FROM_EMAIL = get_env_variable('DEFAULT_FROM_EMAIL')

'''
THIRD PARTY VENDOR Files requre following flag (21.12.2018)
'''
VENDOR_CDN = get_env_variable('VENDOR_CDN', default=False, var_type='bool')

'''
Theme, see also:
http://rdmo.readthedocs.io/en/latest/configuration/themes.html
'''

THEME_APP = get_env_variable('THEME_APP', default='theme')
INSTALLED_APPS.insert(0, THEME_APP)

'''
Export Formats
'''

from django.utils.translation import ugettext_lazy as _
EXPORT_FORMATS = (
    ('pdf', _('PDF')),
    ('rtf', _('Rich Text Format')),
    ('odt', _('Open Office')),
    ('docx', _('Microsoft Office')),
    ('html', _('HTML')),
    ('markdown', _('Markdown')),
    ('mediawiki', _('mediawiki')),
    ('tex', _('LaTeX'))
)

EXPORT_PANDOC_ARGS = {
    'pdf': ['-V', 'geometry:a4paper, margin=2.5cm', '--pdf-engine=xelatex'],
    'rtf': ['--standalone']
}

'''
Import settings
'''
DATA_UPLOAD_MAX_NUMBER_FIELDS = get_env_variable('DATA_UPLOAD_MAX_NUMBER_FIELDS', default=3000, var_type='int')

'''
Cache, see also:
http://rdmo.readthedocs.io/en/latest/configuration/cache.html
'''

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'rdmo_default'
    },
    'api': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'rdmo_api'
    },
}

'''
Extra RDMO user related settings
add settings for upgrade 1.10 for rdmo/rdmo-pm#563
'''
PROFILE_DELETE = get_env_variable('PROFILE_DELETE', default=False, var_type='bool')
ACCOUNT_ALLOW_USER_TOKEN = get_env_variable('ACCOUNT_ALLOW_USER_TOKEN', default=False, var_type='bool')
PROJECT_QUESTIONS_AUTOSAVE = get_env_variable('PROJECT_QUESTIONS_AUTOSAVE', default=False, var_type='bool')


'''
Extra modules
'''
ENABLE_CATALOGS_TABLE_APP = get_env_variable('ENABLE_CATALOGS_TABLE_APP', default=False, var_type='bool')

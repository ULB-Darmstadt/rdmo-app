import os

from pathlib import Path

from rdmo.core.utils import sanitize_url

from dotenv import load_dotenv

LOAD_DEBUG_ENV = os.environ.get('LOAD_DEBUG_ENV', False)

if LOAD_DEBUG_ENV:
    print(f'\n=== LOAD_DEBUG_ENV=True, using .DEBUG.env ===\n')
    load_dotenv('.DEBUG.env')
else:
    load_dotenv('.env')

'''
Use of environment variables
https://github.com/feldroy/two-scoops-of-django-3.x/blob/master/code/chapter_05_example_16.py
'''
# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name, default=None, var_type='str'):
    """Get the environment variable or return exception if no default value is given."""
    try:
        env_var = os.environ[var_name]
        if var_type == 'int':
            env_var = int(env_var)
        elif var_type == 'bool':
            env_var = env_var.upper() == 'TRUE'

        return env_var
    except KeyError:
        
        if default != None:
            return default
        error_msg = 'Missing key and default.\nPlease set the {} environment variable'.format(var_name)
        raise ImproperlyConfigured(error_msg)


SITE_ID = get_env_variable('SITE_ID', var_type='int')

'''
Path settings using pathlib
https://github.com/feldroy/two-scoops-of-django-3.x/blob/master/code/chapter_05_example_29.py
'''
# set path-dependend settings
PROJECT_DIR = BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = PROJECT_DIR.parent
MEDIA_ROOT = BASE_DIR / 'media_root'
STATIC_ROOT = BASE_DIR / 'static_root'
FIXTURE_DIRS = (
    BASE_DIR / 'fixtures',
)

# import default settings from rdmo
from rdmo.core.settings import *

# update STATICFILES_DIRS for the vendor directory
STATICFILES_DIRS = [
    BASE_DIR / 'vendor/'
]

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
RDMO default URI prefix
https://rdmo.readthedocs.io/en/latest/management/index.html
e.g. 'https://rdmo.uni-abc.de/terms/'
'''

DEFAULT_URI_PREFIX = get_env_variable('DEFAULT_URI_PREFIX')

'''
Language code and time zone
'''
LANGUAGE_CODE = 'de-de'
TIME_ZONE = 'Europe/Berlin'


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
Logging configuration
Added logging.handlers.WatchedFileHandler to handlers for log rotation
'''

LOGGING_DIR = BASE_DIR / 'log'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s: %(message)s'
        },
        'name': {
            'format': '[%(asctime)s] %(levelname)s %(name)s: %(message)s'
        },
        'console': {
            'format': '[%(asctime)s] %(message)s'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'error_log': {
            'level': 'ERROR',
            'class':'logging.handlers.WatchedFileHandler',
            'filename': LOGGING_DIR / 'error.log',
            'formatter': 'default'
        },
        'rdmo_log': {
            'level': 'DEBUG',
            'class':'logging.handlers.WatchedFileHandler',
            'filename': LOGGING_DIR / 'rdmo.log',
            'formatter': 'name'
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins', 'error_log'],
            'level': 'DEBUG',
            'propagate': True
        },
        'rdmo': {
            'handlers': ['rdmo_log','console'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}

'''
Extra settings
'''
DEBUG_TOOLBAR = get_env_variable('DEBUG_TOOLBAR', default=False, var_type='bool')
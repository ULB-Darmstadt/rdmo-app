from os import environ
from pathlib import Path


from dotenv import load_dotenv
from split_settings.tools import include, optional

from .tools import get_env_variable, check_env_file_exists
from .components.auth import get_auth_config


'''
Local Paths, settings using pathlib
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

# update STATICFILES_DIRS for the vendor directory
STATICFILES_DIRS = [
    BASE_DIR / 'vendor/'
]


'''
Environment variables 
Determines if the Production or Debug environment file should be selected.
Checks if the selected .env file exists in the BASE_DIR and loads it.
'''

ENV_FILE_MAPPER = {
    'production': BASE_DIR / '.env',
    'development': BASE_DIR / '.DEBUG.env'
    }

ENV_NAME = get_env_variable('DJANGO_ENV', default='development')

ENV_FILE = ENV_FILE_MAPPER.get(ENV_NAME)

check_env_file_exists(ENV_FILE)
load_dotenv(ENV_FILE, override=True)

# Monkeypatching Django, so stubs will work for all generics,
# see: https://github.com/typeddjango/django-stubs
# django_stubs_ext.monkeypatch()

# Managing environment via `DJANGO_ENV` variable:
environ.setdefault('DJANGO_ENV', 'development')
_ENV = environ['DJANGO_ENV']

auth_module = get_auth_config()
# breakpoint()

_base_settings = (
    'components/base.py',
    'components/logging.py',
    # 'components/csp.py',
    'components/auth/{0}.py'.format(auth_module),


    # Select the right env:
    'environments/{0}.py'.format(_ENV),

    # Optionally override some settings:
    # optional('environments/local.py'),
)



# Include settings:
include(*_base_settings)
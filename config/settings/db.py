
'''
The database connection to be used, see also:
http://rdmo.readthedocs.io/en/latest/configuration/databases.html
'''
try:
    if HOME_IMAGES:
        _version_name = '30'
except NameError:
    _version_name = f"{parse(rdmo_version).major}{parse(rdmo_version).minor}"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': f'rdmo_dev_db_{_version_name}.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': '',
#         'USER': '',
#         'PASSWORD': '',
#         'HOST': '',
#         'PORT': '',
#     }
# }
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': f'rdmorganiser_{_version_name}',
#         'USER': 'rdmorganiser_user',
#         'PASSWORD': 'rdmorganiser_password',
#         'HOST': 'localhost',
#         'PORT': '3306',
#         'OPTIONS': {
#             'charset': 'utf8mb4',
#         },
#     }
# }

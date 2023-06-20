
'''
Logging configuration
Added logging.handlers.WatchedFileHandler to handlers for log rotation
'''

LOGGING_DIR = get_env_variable('LOGGING_DIR', default=BASE_DIR / 'log',var_type='path')
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

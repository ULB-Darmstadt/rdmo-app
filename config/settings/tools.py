import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

'''
Using environment variables for the django settings
Adapted from:
https://github.com/feldroy/two-scoops-of-django-3.x/blob/master/code/chapter_05_example_16.py
'''

def get_env_variable(var_name: str, default=None, var_type: str='str'):
    """Get the environment variable or return exception if no default value is given."""

    # print(f'{var_name}: , {default}, {var_type}')
    try:
        env_var = os.environ[var_name]
        # print(f'{var_name}: {env_var}, {default}, {var_type}')
        if var_type == 'int':
            env_var = int(env_var)
        elif var_type == 'bool':
            env_var = env_var.upper() == 'TRUE'
        elif var_type == 'path':
            env_var = Path(env_var).resolve()
            if not env_var.exists() and default == None:
                error_msg = 'Path {} does not exists.\nPlease change the {} environment variable to an existing file'.format(env_var, var_name)
                raise ImproperlyConfigured(error_msg)
            elif not env_var.exists() and default != None:
                return default
        elif var_type == 'str':
            pass
        else:
            error_msg = 'var_type {} does not exists.\nPlease change the {} environment variable setting to an existing var_type'.format(var_type, var_name)
            raise ImproperlyConfigured(error_msg)

        return env_var
    except KeyError:
        
        if default != None:
            return default
        error_msg = 'Missing key and default.\nPlease set the {} environment variable'.format(var_name)
        raise ImproperlyConfigured(error_msg)

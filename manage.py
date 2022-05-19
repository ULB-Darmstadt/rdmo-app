#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    
    LOAD_DEBUG_ENV = os.environ.get('LOAD_DEBUG_ENV', False)
    if LOAD_DEBUG_ENV:
        # print(f'\n=== LOAD_DEBUG_ENV=True, using .DEBUG.env ===\n')
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.debug")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

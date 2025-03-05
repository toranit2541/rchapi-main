"""
WSGI config for rchapi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys

# Add your project directory to the sys.path
sys.path.append('/home/toranit/rchapi-main')

# Activate the virtual environment
activate_this = '/home/toranit/rchapi-main/venv/bin/activate_this.py'
exec(open(activate_this).read(), dict(__file__=activate_this))

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'rchapi-main.settings'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application # type: ignore
application = get_wsgi_application()


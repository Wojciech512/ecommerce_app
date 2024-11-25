"""
WSGI config for ecommerce project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
settings_module =  'ecommerce.deployment' if 'WEBSITE_HOSTNAME' in os.environ else 'ecommerce.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

application = get_wsgi_application()

"""
WSGI config for duty_register project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'duty_register.settings.development')

application = get_wsgi_application()
application = DjangoWhiteNoise(application)

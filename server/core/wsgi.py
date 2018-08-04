"""
WSGI config for base project.

"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.core.settings.dev")

if os.environ.get('SENTRY_DSN', None):
    from raven.contrib.django.raven_compat.middleware.wsgi import Sentry
    application = Sentry(get_wsgi_application())
else:
    application = get_wsgi_application()

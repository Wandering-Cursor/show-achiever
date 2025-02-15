"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import pathlib
import sys

from django.core.asgi import get_asgi_application

sys.path += [
    str(pathlib.Path(__file__).parent.parent),
]

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings.local")

django_app = get_asgi_application()

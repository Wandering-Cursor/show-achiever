"""
Django settings for myapp project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
# ruff: noqa: F403, F405

import dj_database_url

from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    "*",
]

CSRF_TRUSTED_ORIGINS = [
    "https://*.ngrok-free.app",
    "http://localhost",
]


MIDDLEWARE = [*MIDDLEWARE]

DATABASES["default"] = dj_database_url.parse(
    DB_URL,
    conn_health_checks=True,
    ssl_require=False,
)

CACHES["default"]["LOCATION"] = [
    str(settings.cache_connection),
]

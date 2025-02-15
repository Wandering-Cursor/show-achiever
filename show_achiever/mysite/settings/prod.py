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

DEBUG = False

ALLOWED_HOSTS = [
    "*",
]

CSRF_TRUSTED_ORIGINS = security_settings.csrf_trusted_origins

MIDDLEWARE = [*MIDDLEWARE]


DATABASES["default"] = dj_database_url.parse(
    DB_URL,
    # Tweak this setting to meet your needs
    conn_max_age=10,
    conn_health_checks=True,
    ssl_require=True,
)


CACHES["default"]["LOCATION"] = [
    str(settings.cache_connection),
]

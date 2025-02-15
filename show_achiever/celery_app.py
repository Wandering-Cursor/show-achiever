import logging.config
import os

import celery
from mysite.logs import LOGGING

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "mysite.settings.local",
)

celery_app = celery.Celery(
    __name__,
)

celery_app.config_from_object("show_achiever.celeryconfig")

logging.config.dictConfig(LOGGING)

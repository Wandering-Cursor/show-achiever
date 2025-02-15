"""
Basic config for Celery.
"""

from celery.utils.log import get_logger
from mysite.config import settings

logger = get_logger(__name__)

broker_url = settings.broker_url

imports = ("show_achiever.tasks",)

accept_content = ["json", "pickle"]

task_serializer = "json"

enable_utc = True
timezone = settings.timezone_name

broker_connection_retry_on_startup = True

beat_schedule = {}

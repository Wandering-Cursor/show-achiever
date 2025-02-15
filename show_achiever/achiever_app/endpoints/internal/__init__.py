# ruff: noqa: E501

"""
Internal endpoints are mounted to the `app` (with no prefix), and are intended to be used for internal health checks and monitoring.
They are not intended to be exposed to the public internet. (if you use a reverse proxy with a proxy pass that is)

You can add inter-server communication endpoints here, or any other internal endpoints that you want to keep separate from the rest of your API.
"""

from . import healthz

__all__ = [
    "healthz",
]

"""
Endpoints for tasks.

Creating a task means that the user has completed a task.
This is done by scanning a QR code for that task (Partner Task Item entity).
"""

from . import create

__all__ = [
    "create",
]

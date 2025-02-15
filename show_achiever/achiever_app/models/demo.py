from django.db import models
from achiever_app.models.base import BaseModel


class DemoModel(BaseModel):
    name = models.CharField(max_length=255)

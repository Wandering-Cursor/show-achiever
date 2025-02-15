from typing import Literal

from achiever_app.schemas.base import Schema


class HealthSchema(Schema):
    status: Literal["ok"] = "ok"

import pydantic
from achiever_app.schemas.base import Schema


class CompleteTaskRequest(Schema):
    attendee_id: int


class CompleteTaskResponse(Schema):
    task_id: pydantic.UUID4
    completed: bool

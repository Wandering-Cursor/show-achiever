from mysite.errors.database_errors import DatabaseIntegrityError


class TaskItemUsedError(DatabaseIntegrityError):
    error_name: str = "TaskItemUsedError"
    error_message: str = "Task item is already used"

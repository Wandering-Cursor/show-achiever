import math

from telegram_bot_app.schemas.base import Schema


class PaginationMeta(Schema):
    page: int
    per_page: int
    total: int

    @property
    def pages(self) -> int:
        return math.ceil(self.total / self.per_page)

    @property
    def next_page(self) -> int | None:
        return self.page + 1 if self.page < self.pages else None

    @property
    def previous_page(self) -> int | None:
        return self.page - 1 if self.page > 1 else None

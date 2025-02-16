import asyncio
import uuid

from django.db import models


class SynchronousOnlyAttributeHandler:
    async def _get_attribute_async(self, item: str) -> "object":
        from asgiref.sync import sync_to_async

        sta = sync_to_async(lambda: self.__getattribute__(item))
        return await sta()

    def __getattribute__(self, item: str) -> asyncio.Future[object] | object:
        from django.core.exceptions import SynchronousOnlyOperation

        try:
            return super().__getattribute__(item)
        except SynchronousOnlyOperation:
            if asyncio.get_event_loop().is_running():
                return asyncio.ensure_future(self._get_attribute_async(item))
            return asyncio.run(self._get_attribute_async(item))


class BaseModel(SynchronousOnlyAttributeHandler, models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        get_latest_by = "created_at"
        ordering = ("-created_at",)


class BaseMeta(BaseModel.Meta):
    abstract = False

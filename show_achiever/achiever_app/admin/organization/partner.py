from typing import TYPE_CHECKING

from achiever_app.admin.base import BaseAdmin, NoAddAdminMixin, NoChangeAdminMixin
from achiever_app.models.organization import Partner, PartnerTask, PartnerTaskItem
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from django.db import models


def create_partner_task_items(qs: "models.QuerySet[PartnerTask]", items: int) -> None:
    from django.db import transaction

    for task in qs:
        with transaction.atomic():
            for _iterator in range(items):
                PartnerTaskItem.objects.create(task=task)


@admin.action(description=_("Create Partner Task Items (10)"))
def create_10_partner_task_items(modeladmin, request, queryset) -> None:  # noqa: ANN001, ARG001
    create_partner_task_items(queryset, 10)


@admin.action(description=_("Create Partner Task Items (50)"))
def create_50_partner_task_items(modeladmin, request, queryset) -> None:  # noqa: ANN001, ARG001
    create_partner_task_items(queryset, 50)


@admin.action(description=_("Create Partner Task Items (100)"))
def create_100_partner_task_items(modeladmin, request, queryset) -> None:  # noqa: ANN001, ARG001
    create_partner_task_items(queryset, 100)


class PartnerInline(admin.TabularInline):
    model = Partner
    extra = 0
    show_change_link = True


class PartnerTaskInline(admin.TabularInline):
    model = PartnerTask
    extra = 0
    show_change_link = True


class PartnerTakItemInline(NoAddAdminMixin, NoChangeAdminMixin, admin.TabularInline):
    model = PartnerTaskItem
    extra = 0


@admin.register(PartnerTaskItem)
class PartnerTaskItemAdmin(NoChangeAdminMixin, BaseAdmin):
    fieldsets = (
        *BaseAdmin.fieldsets,
        (
            _("Partner Task Item"),
            {
                "fields": (
                    "task",
                    "is_used",
                )
            },
        ),
    )

    list_display = (
        *BaseAdmin.list_display[: BaseAdmin.LIST_DISPLAY_START],
        "task",
        "is_used",
        *BaseAdmin.list_display[BaseAdmin.LIST_DISPLAY_END :],
    )

    LIST_DISPLAY_START = BaseAdmin.LIST_DISPLAY_START + 2


@admin.register(PartnerTask)
class PartnerTaskAdmin(BaseAdmin):
    fieldsets = (
        *BaseAdmin.fieldsets,
        (
            _("Partner Task"),
            {
                "fields": (
                    "partner",
                    "name",
                    "description",
                    "image",
                    "reward_currency",
                    "reward_amount",
                )
            },
        ),
    )

    list_display = (
        *BaseAdmin.list_display[: BaseAdmin.LIST_DISPLAY_START],
        "partner",
        "name",
        "reward_currency",
        "reward_amount",
        *BaseAdmin.list_display[BaseAdmin.LIST_DISPLAY_END :],
    )

    LIST_DISPLAY_START = BaseAdmin.LIST_DISPLAY_START + 4

    actions = (
        *BaseAdmin.actions,
        create_10_partner_task_items,
        create_50_partner_task_items,
        create_100_partner_task_items,
    )

    inlines = (
        *BaseAdmin.inlines,
        PartnerTakItemInline,
    )


@admin.register(Partner)
class PartnerAdmin(BaseAdmin):
    fieldsets = (
        *BaseAdmin.fieldsets,
        (
            _("Partner"),
            {
                "fields": (
                    "name",
                    "description",
                    "logo",
                    "for_event",
                )
            },
        ),
    )

    list_display = (
        *BaseAdmin.list_display[: BaseAdmin.LIST_DISPLAY_START],
        "for_event",
        "name",
        *BaseAdmin.list_display[BaseAdmin.LIST_DISPLAY_END :],
    )

    LIST_DISPLAY_START = BaseAdmin.LIST_DISPLAY_START + 2

    inlines = (
        *BaseAdmin.inlines,
        PartnerTaskInline,
    )

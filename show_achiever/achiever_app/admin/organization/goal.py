from achiever_app.admin.base import BaseAdmin
from achiever_app.models.organization import Goal, GoalBalance, GoalTransaction
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


@admin.register(Goal)
class GoalAdmin(BaseAdmin):
    fieldsets = (
        *BaseAdmin.fieldsets,
        (
            _("Goal"),
            {
                "fields": (
                    "name",
                    "description",
                    "poster",
                    "for_event",
                    "current_balance",
                    "required_amount",
                    "currency",
                )
            },
        ),
    )

    list_display = (
        *BaseAdmin.list_display[: BaseAdmin.LIST_DISPLAY_START],
        "for_event",
        "name",
        "description",
        "required_amount",
        "currency",
        *BaseAdmin.list_display[BaseAdmin.LIST_DISPLAY_END :],
    )

    readonly_fields = (
        *BaseAdmin.readonly_fields,
        "current_balance",
    )

    LIST_DISPLAY_START = BaseAdmin.LIST_DISPLAY_START + 5


@admin.register(GoalTransaction)
class GoalTransactionAdmin(BaseAdmin):
    fieldsets = (
        *BaseAdmin.fieldsets,
        (
            _("Goal Transaction"),
            {
                "fields": (
                    "goal",
                    "amount",
                    "from_attendee_balance",
                )
            },
        ),
    )

    list_display = (
        *BaseAdmin.list_display[: BaseAdmin.LIST_DISPLAY_START],
        "goal",
        "amount",
        "from_attendee_balance",
        *BaseAdmin.list_display[BaseAdmin.LIST_DISPLAY_END :],
    )

    LIST_DISPLAY_START = BaseAdmin.LIST_DISPLAY_START + 3


@admin.register(GoalBalance)
class GoalBalanceAdmin(BaseAdmin):
    fieldsets = (
        *BaseAdmin.fieldsets,
        (
            _("Goal Balance"),
            {
                "fields": (
                    "goal",
                    "amount",
                    "goal_transaction",
                )
            },
        ),
    )

    list_display = (
        *BaseAdmin.list_display[: BaseAdmin.LIST_DISPLAY_START],
        "goal",
        "amount",
        "goal_transaction",
        *BaseAdmin.list_display[BaseAdmin.LIST_DISPLAY_END :],
    )

    LIST_DISPLAY_START = BaseAdmin.LIST_DISPLAY_START + 3

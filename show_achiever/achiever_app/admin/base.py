from copy import deepcopy
from typing import TYPE_CHECKING

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

if TYPE_CHECKING:
    import django.db.models
    import django.http


class BaseAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "uuid",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    list_display = (
        "uuid",
        "created_at",
        "updated_at",
    )
    list_display_links = ("uuid",)

    list_filter = ("created_at", "updated_at")
    ordering = ("-created_at",)
    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
    )

    list_per_page = 25
    djangoql_completion_enabled_by_default = True
    KEEP_LIST_DISPLAY = 1


class NoViewAdminMixin:
    def has_view_permission(
        self: "NoViewAdminMixin",
        request: "django.http.HttpRequest",  # noqa: ARG002
        obj: "django.db.models.Model | None" = None,  # noqa: ARG002
    ) -> bool:
        return False


class NoAddAdminMixin:
    def has_add_permission(
        self: "ReadOnlyAdminMixin",
        request: "django.http.HttpRequest",  # noqa: ARG002
        *args: "django.db.models.Model",  # noqa: ARG002
    ) -> bool:
        return False


class NoChangeAdminMixin:
    def has_change_permission(
        self: "NoChangeAdminMixin",
        request: "django.http.HttpRequest",  # noqa: ARG002
        obj: "django.db.models.Model | None" = None,  # noqa: ARG002
    ) -> bool:
        return False


class NoDeletesAdminMixin:
    def has_delete_permission(
        self: "NoDeletesAdminMixin",
        request: "django.http.HttpRequest",  # noqa: ARG002
        obj: "django.db.models.Model | None" = None,  # noqa: ARG002
    ) -> bool:
        return False


class NoEditsAdminMixin(NoChangeAdminMixin, NoDeletesAdminMixin):
    pass


class ReadOnlyAdminMixin(NoAddAdminMixin, NoEditsAdminMixin):
    pass


class NotAvailableAdminMixin:
    def has_module_permission(
        self: "NotAvailableAdminMixin",
        request: "django.http.HttpRequest",  # noqa: ARG002
    ) -> bool:
        return False


def linkify(field_name: str, visible_name: str = "") -> str:
    """
    Converts a foreign key value into clickable links.

    If field_name is 'parent', link text will be str(obj.parent)
    Link will be admin url for the admin url for obj.parent.id:change
    """

    def _linkify(*args: "django.db.models.Model | admin.ModelAdmin") -> str:
        args_when_used_inf_fields = 2
        is_used_in_fields = len(args) == args_when_used_inf_fields

        obj: django.db.models.Model = args[1] if is_used_in_fields else args[0]

        linked_obj: django.db.models.Model | None = getattr(obj, field_name)
        if linked_obj is None:
            return "-"
        app_label = linked_obj._meta.app_label  # noqa: SLF001
        model_name = linked_obj._meta.model_name  # noqa: SLF001

        view_name = f"admin:{app_label}_{model_name}_change"
        link_url = reverse(view_name, args=[linked_obj.pk])

        return format_html('<a href="{}">{}</a>', link_url, linked_obj)

    _linkify.short_description = visible_name or field_name
    return _linkify


def flatten_fieldsets(fieldsets: tuple[tuple[str, dict[str, str]]]) -> list[str]:
    return [field for _, fields in fieldsets for field in fields["fields"]]


def exclude_field(fields: list[str], exclude: list[str]) -> list[str]:
    return [field for field in fields if field not in exclude]


def append_to_fieldset(
    fieldsets: tuple[tuple[str, dict[str, str]]],
    name: str | None,
    fields: list[str],
) -> tuple[tuple[str, dict[str, str]]]:
    fieldsets = deepcopy(fieldsets)
    new_fieldsets = []

    for title, fieldset in fieldsets:
        if title == name:
            fields.extend(fieldset["fields"])
            fieldset["fields"] = fields
        new_fieldsets.append((title, fieldset))

    return tuple(new_fieldsets)

from achiever_app.models.common import EventAdmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class EventAdminInline(admin.StackedInline):
    model = EventAdmin
    can_delete = False
    verbose_name_plural = _("Event Admins")


class UserAdmin(BaseUserAdmin):
    inlines = (
        *BaseUserAdmin.inlines,
        EventAdminInline,
    )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

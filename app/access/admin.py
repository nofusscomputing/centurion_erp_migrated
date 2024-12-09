from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin

from .models import *

admin.site.unregister(Group)

class TeamInline(admin.TabularInline):
    model = Team
    extra = 0

    readonly_fields = ['name', 'created', 'modified']
    fields = ['team_name']

    fk_name = 'organization'


class OrganizationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name", 'manager', "slug"]}),
        #("Date information", {"fields": ["slug"], "classes": ["collapse"]}),
    ]
    inlines = [TeamInline]
    list_display = ["name", "created", "modified"]
    list_filter = ["created"]
    search_fields = ["team_name"]

admin.site.register(Organization,OrganizationAdmin)


class TeamUserInline(admin.TabularInline):
    model = TeamUsers
    extra = 0

    readonly_fields = ['created', 'modified']
    fields = ['team']

    fk_name = 'user'


admin.site.unregister(User)
class UsrAdmin(UserAdmin):

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
                
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    inlines = [TeamUserInline]

admin.site.register(User,UsrAdmin)


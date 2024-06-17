from django.contrib import admin
from django.contrib.auth.models import Group

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


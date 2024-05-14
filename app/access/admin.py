from django.contrib import admin
from django.contrib.auth.models import Group

from .models import *


class TeamInline(admin.TabularInline):
    model = Team
    extra = 0

    readonly_fields = ['name', 'created', 'modified']
    fields = ['team_name']

    fk_name = 'organization'


class OrganizationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name", "slug"]}),
        #("Date information", {"fields": ["slug"], "classes": ["collapse"]}),
    ]
    inlines = [TeamInline]
    list_display = ["name", "created", "modified"]
    list_filter = ["created"]
    search_fields = ["team_name"]


admin.site.register(Organization,OrganizationAdmin)


class UserInline(admin.TabularInline):
    model = TeamUsers
    extra = 0

    fk_name = 'team'

    readonly_fields = ['created', 'modified']



class TeamAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["organization", 'name', "team_name", 'permissions']}),
        #("Date information", {"fields": ["slug"], "classes": ["collapse"]}),
    ]
    inlines = [UserInline]
    list_display = ["team_name", "created", "modified"]
    list_filter = ["created"]
    search_fields = ["name"]
    readonly_fields = ['organization', 'name']

admin.site.register(Team,TeamAdmin)

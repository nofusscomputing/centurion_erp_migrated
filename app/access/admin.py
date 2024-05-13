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

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        #  if db_field.name == "permission":
        #     # limited_choices = [(choice[0], choice[1]) for choice in Permission if choice[0] == 1 or choice[0] == 5]
        #     # kwargs['permission'] = forms.ChoiceField(choices=limited_choices)
        kwargs["permissions"] = Permission.objects.filter(id=5)
        return super(TeamAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Team,TeamAdmin)

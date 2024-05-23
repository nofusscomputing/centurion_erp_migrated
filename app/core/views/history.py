import markdown

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import generic

from access.mixin import OrganizationPermission

from core.models.history import History

from itam.models.device import Device, DeviceSoftware, DeviceOperatingSystem
from itam.models.software import Software


class View(OrganizationPermission, generic.View):

    permission_required = [
        'itam.view_softwareversion'
    ]

    template_name = 'history.html.j2'


    def get(self, request, model_name, model_pk):
        if not request.user.is_authenticated and settings.LOGIN_REQUIRED:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")

        context = {}

        context['history'] = History.objects.filter(
            Q(item_pk = model_pk, item_class = model_name)
            |
            Q(item_parent_pk = model_pk, item_parent_class = model_name)
        )

        context['content_title'] = 'History'

        return render(request, self.template_name, context)

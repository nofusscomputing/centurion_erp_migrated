from django.contrib.auth.middleware import (
    AuthenticationMiddleware,
    SimpleLazyObject,
    partial,
)

from settings.models.app_settings import AppSettings


class AuthenticationMiddleware(AuthenticationMiddleware):


    def process_request(self, request):

        super().process_request(request)

        request.app_settings = AppSettings.objects.select_related('global_organization').get(
            owner_organization = None
        )

"""
URL configuration for itsm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.static import serve
from django.urls import include, path, re_path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import home

from core.views import history

from settings.views import user_settings



urlpatterns = [
    path('', home.HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls, name='_administration'),

    path('account/password_change/', auth_views.PasswordChangeView.as_view(template_name="password_change.html.j2"), name="change_password"),
    path('account/settings/<int:pk>', user_settings.View.as_view(), name="_settings_user"),
    path('account/settings/<int:pk>/edit', user_settings.Change.as_view(), name="_settings_user_change"),
    path('account/settings/<int:user_id>/token/add', user_settings.TokenAdd.as_view(), name="_user_auth_token_add"),
    path('account/settings/<int:user_id>/token/<int:pk>/delete', user_settings.TokenDelete.as_view(), name="_user_auth_token_delete"),
    path("account/", include("django.contrib.auth.urls")),

    path("organization/", include("access.urls")),
    path("itam/", include("itam.urls")),
    path("config_management/", include("config_management.urls")),

    path("history/<str:model_name>/<int:model_pk>", history.View.as_view(), name='_history'),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

]


if settings.SSO_ENABLED:

    urlpatterns += [
        path('sso/', include('social_django.urls', namespace='social'))
    ]


if settings.API_ENABLED:
    urlpatterns += [

        path("api/", include("api.urls")),
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    ]


if settings.DEBUG:

    urlpatterns += [

        path("__debug__/", include("debug_toolbar.urls"), name='_debug'),
        # Apps Under Development
        path("itim/", include("itim.urls")),
        path("information/", include("information.urls")),
        path("project_management/", include("project_management.urls")),
    ]

# must be after above
urlpatterns += [

    path("settings/", include("settings.urls")),

]

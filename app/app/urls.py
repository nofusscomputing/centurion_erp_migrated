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
from django.urls import include, path

from .views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path("api/", include("api.urls")),
    path('admin/', admin.site.urls, name='_administration'),
    path('account/password_change/', auth_views.PasswordChangeView.as_view(template_name="password_change.html.j2"),
         name="change_password"),
    path("account/", include("django.contrib.auth.urls")),
    path("organization/", include("access.urls")),
]

if settings.DEBUG:

    urlpatterns += [

        path("__debug__/", include("debug_toolbar.urls"), name='_debug'),
    ]

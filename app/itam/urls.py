from django.urls import path

from . import views
from .views import device, device_type, software, software_category, software_version

app_name = "ITAM"
urlpatterns = [

    path("device/", device.IndexView.as_view(), name="Devices"),

    path("device/<int:pk>/", device.View.as_view(), name="_device_view"),
    path("device/<int:pk>/software/add", device.SoftwareAdd.as_view(), name="_device_software_add"),
    path("device/<int:device_id>/software/<int:pk>", device.SoftwareView.as_view(), name="_device_software_view"),

    path("device/<int:pk>/delete", device.Delete.as_view(), name="_device_delete"),
    path("device/add/", device.Add.as_view(), name="_device_add"),

    path("device_type/add/", device_type.Add.as_view(), name="_device_type_add"),

    path("software/", software.IndexView.as_view(), name="Software"),
    path("software/<int:pk>/", software.View.as_view(), name="_software_view"),
    path("software/<int:pk>/delete", software.Delete.as_view(), name="_software_delete"),
    path("software/<int:pk>/version/add", software_version.Add.as_view(), name="_software_version_add"),
    path("software/add/", software.Add.as_view(), name="_software_add"),

    path("software_category/add/", software_category.Add.as_view(), name="_software_category_add"),

]

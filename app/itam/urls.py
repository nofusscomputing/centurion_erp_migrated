from django.urls import path

from . import views
from .views import device, device_type, software, software_category, software_version, operating_system, operating_system_version

app_name = "ITAM"
urlpatterns = [

    path("device/", device.IndexView.as_view(), name="Devices"),

    path("device/<int:pk>/", device.View.as_view(), name="_device_view"),
    path("device/<int:pk>/edit", device.Change.as_view(), name="_device_change"),
    path("device/<int:pk>/software/add", device.SoftwareAdd.as_view(), name="_device_software_add"),
    path("device/<int:device_id>/software/<int:pk>", device.SoftwareView.as_view(), name="_device_software_view"),
    path("device/<int:pk>/delete", device.Delete.as_view(), name="_device_delete"),
    path("device/add/", device.Add.as_view(), name="_device_add"),


    path("operating_system", operating_system.IndexView.as_view(), name="Operating Systems"),
    path("operating_system/<int:pk>", operating_system.View.as_view(), name="_operating_system_view"),
    path("operating_system/add", operating_system.Add.as_view(), name="_operating_system_add"),
    path("operating_system/delete/<int:pk>", operating_system.Delete.as_view(), name="_operating_system_delete"),


    path("operating_system/<int:operating_system_id>/version/<int:pk>", operating_system_version.View.as_view(), name="_operating_system_version_view"),
    path("operating_system/<int:pk>/version/add", operating_system_version.Add.as_view(), name="_operating_system_version_add"),
    path("operating_system/<int:operating_system_id>/version/<int:pk>/delete", operating_system_version.Delete.as_view(), name="_operating_system_version_delete"),
    


    path("software/", software.IndexView.as_view(), name="Software"),
    path("software/<int:pk>/", software.View.as_view(), name="_software_view"),
    path("software/<int:pk>/delete", software.Delete.as_view(), name="_software_delete"),
    path("software/<int:pk>/version/add", software_version.Add.as_view(), name="_software_version_add"),
    path("software/<int:software_id>/version/<int:pk>", software_version.View.as_view(), name="_software_version_view"),
    path("software/add/", software.Add.as_view(), name="_software_add"),

]

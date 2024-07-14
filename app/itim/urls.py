from django.urls import path

from itam import views
from itam.views import device, device_type, software, software_category, software_version, operating_system, operating_system_version

app_name = "ITIM"
urlpatterns = [

    # path("clusters", device.IndexView.as_view(), name="Clusters"),
    # path("services", device.IndexView.as_view(), name="Services"),

]

from django.urls import path

from .views import home

app_name = "Settings"
urlpatterns = [

    path("", home.View.as_view(), name="Settings"),

]

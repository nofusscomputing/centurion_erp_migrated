from django.urls import path

from . import views

app_name = "structure"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.OrganizationView.as_view(), name="organization"),
]

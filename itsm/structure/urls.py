from django.urls import path

from . import views

app_name = "Structure"
urlpatterns = [
    path("", views.IndexView.as_view(), name="Organizations"),
    path("<int:pk>/", views.OrganizationView.as_view()),
]

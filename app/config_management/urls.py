from django.urls import path

from .views import ConfigIndex

app_name = "Config Management"
urlpatterns = [
    path('', ConfigIndex.as_view(), name='Config Management'),
    
]

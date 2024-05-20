from django.urls import path

from . import views
from .views import knowledge_base, playbooks

app_name = "Information"

urlpatterns = [

    path("kb/", knowledge_base.Index.as_view(), name="Knowledge Base"),
    path("playbook/", playbooks.Index.as_view(), name="Playbooks"),

]

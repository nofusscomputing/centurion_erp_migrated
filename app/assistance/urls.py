from django.urls import path

from assistance.views import knowledge_base

app_name = "Assistance"

urlpatterns = [

    path("information", knowledge_base.Index.as_view(), name="Knowledge Base"),

]

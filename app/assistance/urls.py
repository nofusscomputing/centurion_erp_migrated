from django.urls import path

from assistance.views import knowledge_base

app_name = "Assistance"

urlpatterns = [

    path("information", knowledge_base.Index.as_view(), name="Knowledge Base"),
    path("information/add", knowledge_base.Add.as_view(), name="_knowledge_base_add"),
    path("information/<int:pk>/edit", knowledge_base.Change.as_view(), name="_knowledge_base_change"),
    path("information/<int:pk>/delete", knowledge_base.Delete.as_view(), name="_knowledge_base_delete"),
    path("information/<int:pk>", knowledge_base.View.as_view(), name="_knowledge_base_view"),

]

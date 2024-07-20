from django.urls import path


from itim.views import services

app_name = "ITIM"
urlpatterns = [

    path("services", services.Index.as_view(), name="Services"),
    path("service/add", services.Add.as_view(), name="_service_add"),
    path("service/<int:pk>/edit", services.Change.as_view(), name="_service_change"),
    path("service/<int:pk>/delete", services.Delete.as_view(), name="_service_delete"),
    path("service/<int:pk>", services.View.as_view(), name="_service_view"),

]

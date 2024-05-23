from django.urls import path

from .views import home, device_types, software_categories

from itam.views import device_type, software_category

app_name = "Settings"
urlpatterns = [

    path("", home.View.as_view(), name="Settings"),

    path("device_type/", device_types.Index.as_view(), name="_device_types"),
    path("device_type/<int:pk>", device_type.View.as_view(), name="_device_type_view"),
    path("device_type/add/", device_type.Add.as_view(), name="_device_type_add"),
    path("device_type/<int:pk>/delete", device_type.Delete.as_view(), name="_device_type_delete"),

    path("software_category", software_categories.Index.as_view(), name="_software_categories"),
    path("software_category/<int:pk>", software_category.View.as_view(), name="_software_category_view"),
    path("software_category/add/", software_category.Add.as_view(), name="_software_category_add"),
    path("software_category/<int:pk>/delete", software_category.Delete.as_view(), name="_software_category_delete"),

]

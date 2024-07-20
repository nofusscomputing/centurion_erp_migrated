from django.urls import path

from assistance.views import knowledge_base_category

from core.views import celery_log

from settings.views import app_settings, home, device_models, device_types, external_link, manufacturer, software_categories

from itam.views import device_type, device_model, software_category

from itim.views import ports

app_name = "Settings"
urlpatterns = [

    path("", home.View.as_view(), name="Settings"),

    path("external_links", external_link.Index.as_view(), name="External Links"),
    path("external_links/add", external_link.Add.as_view(), name="_external_link_add"),
    path("external_links/<int:pk>", external_link.View.as_view(), name="_external_link_view"),
    path("external_links/<int:pk>/edit", external_link.Change.as_view(), name="_external_link_change"),
    path("external_links/<int:pk>/delete", external_link.Delete.as_view(), name="_external_link_delete"),


    path('application', app_settings.View.as_view(), name="_settings_application"),
    
    path("task_results", celery_log.Index.as_view(), name="_task_results"),
    path("task_result/<int:pk>", celery_log.View.as_view(), name="_task_result_view"),

    path("device_models", device_models.Index.as_view(), name="_device_models"),
    path("device_model/<int:pk>", device_model.View.as_view(), name="_device_model_view"),
    path("device_model/add/", device_model.Add.as_view(), name="_device_model_add"),
    path("device_model/<int:pk>/delete", device_model.Delete.as_view(), name="_device_model_delete"),

    path("device_type/", device_types.Index.as_view(), name="_device_types"),
    path("device_type/<int:pk>", device_type.View.as_view(), name="_device_type_view"),
    path("device_type/add/", device_type.Add.as_view(), name="_device_type_add"),
    path("device_type/<int:pk>/delete", device_type.Delete.as_view(), name="_device_type_delete"),

    path("kb/category", knowledge_base_category.Index.as_view(), name="KB Categories"),
    path("kb/category/add", knowledge_base_category.Add.as_view(), name="_knowledge_base_category_add"),
    path("kb/category/<int:pk>/edit", knowledge_base_category.Change.as_view(), name="_knowledge_base_category_change"),
    path("kb/category/<int:pk>/delete", knowledge_base_category.Delete.as_view(), name="_knowledge_base_category_delete"),
    path("kb/category/<int:pk>", knowledge_base_category.View.as_view(), name="_knowledge_base_category_view"),

    path("software_category", software_categories.Index.as_view(), name="_software_categories"),
    path("software_category/<int:pk>", software_category.View.as_view(), name="_software_category_view"),
    path("software_category/add/", software_category.Add.as_view(), name="_software_category_add"),
    path("software_category/<int:pk>/delete", software_category.Delete.as_view(), name="_software_category_delete"),

    path("manufacturers", manufacturer.Index.as_view(), name="_manufacturers"),
    path("manufacturer/<int:pk>", manufacturer.View.as_view(), name="_manufacturer_view"),
    path("manufacturer/add/", manufacturer.Add.as_view(), name="_manufacturer_add"),
    path("manufacturer/<int:pk>/delete", manufacturer.Delete.as_view(), name="_manufacturer_delete"),

    path("ports", ports.Index.as_view(), name="_ports"),
    path("port/add", ports.Add.as_view(), name="_port_add"),
    path("port/<int:pk>/edit", ports.Change.as_view(), name="_port_change"),
    path("port/<int:pk>/delete", ports.Delete.as_view(), name="_port_delete"),
    path("port/<int:pk>", ports.View.as_view(), name="_port_view"),

]

from django.urls import path

from config_management.views.groups.groups import GroupIndexView, GroupAdd, GroupDelete, GroupView, GroupHostAdd, GroupHostDelete
from config_management.views.groups.software import GroupSoftwareAdd, GroupSoftwareChange, GroupSoftwareDelete

app_name = "Config Management"

urlpatterns = [
    path('group', GroupIndexView.as_view(), name='Groups'),
    path('group/add', GroupAdd.as_view(), name='_group_add'),
    path('group/<int:pk>', GroupView.as_view(), name='_group_view'),

    path('group/<int:pk>/child', GroupAdd.as_view(), name='_group_add_child'),
    path('group/<int:pk>/delete', GroupDelete.as_view(), name='_group_delete'),

    path("group/<int:pk>/software/add", GroupSoftwareAdd.as_view(), name="_group_software_add"),
    path("group/<int:group_id>/software/<int:pk>", GroupSoftwareChange.as_view(), name="_group_software_change"),
    path("group/<int:group_id>/software/<int:pk>/delete", GroupSoftwareDelete.as_view(), name="_group_software_delete"),

    path('group/<int:pk>/host', GroupHostAdd.as_view(), name='_group_add_host'),
    path('group/<int:group_id>/host/<int:pk>/delete', GroupHostDelete.as_view(), name='_group_delete_host'),

]

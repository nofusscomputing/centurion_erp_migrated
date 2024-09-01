from django.urls import path

from config_management.views.groups import groups
from config_management.views.groups.groups import GroupHostAdd, GroupHostDelete

from config_management.views.groups import software
# from config_management.views.groups.software import GroupSoftwareAdd, GroupSoftwareChange, GroupSoftwareDelete

app_name = "Config Management"

urlpatterns = [
    path('group', groups.Index.as_view(), name='Groups'),
    path('group/add', groups.Add.as_view(), name='_group_add'),
    path('group/<int:pk>', groups.View.as_view(), name='_group_view'),
    path('group/<int:pk>/edit', groups.Change.as_view(), name='_group_change'),

    path('group/<int:pk>/child', groups.Add.as_view(), name='_group_add_child'),
    path('group/<int:pk>/delete', groups.Delete.as_view(), name='_group_delete'),

    path("group/<int:pk>/software/add", software.Add.as_view(), name="_group_software_add"),
    path("group/<int:group_id>/software/<int:pk>", software.Change.as_view(), name="_group_software_change"),
    path("group/<int:group_id>/software/<int:pk>/delete", software.Delete.as_view(), name="_group_software_delete"),

    path('group/<int:pk>/host', GroupHostAdd.as_view(), name='_group_add_host'),
    path('group/<int:group_id>/host/<int:pk>/delete', GroupHostDelete.as_view(), name='_group_delete_host'),

]

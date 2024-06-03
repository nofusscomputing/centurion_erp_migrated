from django.urls import path

from config_management.views.groups import GroupIndexView, GroupAdd, GroupDelete, GroupView, GroupHostAdd, GroupHostDelete

app_name = "Config Management"

urlpatterns = [
    path('group', GroupIndexView.as_view(), name='Groups'),
    path('group/add', GroupAdd.as_view(), name='_group_add'),
    path('group/<int:pk>', GroupView.as_view(), name='_group_view'),
    path('group/<int:group_id>/child', GroupAdd.as_view(), name='_group_add_child'),
    path('group/<int:pk>/delete', GroupDelete.as_view(), name='_group_delete'),

    path('group/<int:group_id>/host', GroupHostAdd.as_view(), name='_group_add_host'),
    path('group/<int:group_id>/host/<int:pk>/delete', GroupHostDelete.as_view(), name='_group_delete_host'),

]

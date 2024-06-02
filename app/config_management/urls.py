from django.urls import path

from config_management.views.index import ConfigIndex
from config_management.views.groups import GroupIndexView, GroupAdd, GroupDelete, GroupView

app_name = "Config Management"

urlpatterns = [
    path('', ConfigIndex.as_view(), name='Config Management'),
    path('group', GroupIndexView.as_view(), name='_group_index'),
    path('group/add', GroupAdd.as_view(), name='_group_add'),
    path('group/<int:pk>', GroupView.as_view(), name='_group_view'),
    path('group/<int:pk>/delete', GroupDelete.as_view(), name='_group_delete'),

]

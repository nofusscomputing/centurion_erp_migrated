from django.urls import path

from core.views import ticket, ticket_comment

from itim.views import clusters, services

app_name = "ITIM"
urlpatterns = [

    path('ticket/change', ticket.Index.as_view(), kwargs={'ticket_type': 'change'}, name="Changes"),
    path('ticket/<str:ticket_type>/add', ticket.Add.as_view(), name="_ticket_change_add"),
    path('ticket/<str:ticket_type>/<int:pk>/edit', ticket.Change.as_view(), name="_ticket_change_change"),
    path('ticket/<str:ticket_type>/<int:pk>/delete', ticket.Delete.as_view(), name="_ticket_change_delete"),
    path('ticket/<str:ticket_type>/<int:pk>', ticket.View.as_view(), name="_ticket_change_view"),
    path('ticket/<str:ticket_type>/<int:ticket_id>/comment/add', ticket_comment.Add.as_view(), name="_ticket_comment_change_add"),
    path('ticket/<str:ticket_type>/<int:ticket_id>/comment/<int:pk>/edit', ticket_comment.Change.as_view(), name="_ticket_comment_change_change"),
    path('ticket/<str:ticket_type>/<int:ticket_id>/comment/<int:parent_id>/add', ticket_comment.Add.as_view(), name="_ticket_comment_change_reply_add"),

    path("clusters", clusters.Index.as_view(), name="Clusters"),
    path("clusters/add", clusters.Add.as_view(), name="_cluster_add"),
    path("clusters/<int:pk>/edit", clusters.Change.as_view(), name="_cluster_change"),
    path("clusters/<int:pk>/delete", clusters.Delete.as_view(), name="_cluster_delete"),
    path("clusters/<int:pk>", clusters.View.as_view(), name="_cluster_view"),

    path('ticket/incident', ticket.Index.as_view(), kwargs={'ticket_type': 'incident'}, name="Incidents"),
    path('ticket/<str:ticket_type>/add', ticket.Add.as_view(), name="_ticket_incident_add"),
    path('ticket/<str:ticket_type>/<int:pk>/edit', ticket.Change.as_view(), name="_ticket_incident_change"),
    path('ticket/<str:ticket_type>/<int:pk>/delete', ticket.Delete.as_view(), name="_ticket_incident_delete"),
    path('ticket/<str:ticket_type>/<int:pk>', ticket.View.as_view(), name="_ticket_incident_view"),
    path('ticket/<str:ticket_type>/<int:ticket_id>/comment/add', ticket_comment.Add.as_view(), name="_ticket_comment_incident_add"),
    path('ticket/<str:ticket_type>/<int:ticket_id>/comment/<int:pk>/edit', ticket_comment.Change.as_view(), name="_ticket_comment_incident_change"),
    path('ticket/<str:ticket_type>/<int:ticket_id>/comment/<int:parent_id>/add', ticket_comment.Add.as_view(), name="_ticket_comment_incident_reply_add"),

    path('ticket/problem', ticket.Index.as_view(), kwargs={'ticket_type': 'problem'}, name="Problems"),
    path('ticket/<str:ticket_type>/add', ticket.Add.as_view(), name="_ticket_problem_add"),
    path('ticket/<str:ticket_type>/<int:pk>/edit', ticket.Change.as_view(), name="_ticket_problem_change"),
    path('ticket/<str:ticket_type>/<int:pk>/delete', ticket.Delete.as_view(), name="_ticket_problem_delete"),
    path('ticket/<str:ticket_type>/<int:pk>', ticket.View.as_view(), name="_ticket_problem_view"),
    path('ticket/<str:ticket_type>/<int:ticket_id>/comment/add', ticket_comment.Add.as_view(), name="_ticket_comment_problem_add"),
    path('ticket/<str:ticket_type>/<int:ticket_id>/comment/<int:pk>/edit', ticket_comment.Change.as_view(), name="_ticket_comment_problem_change"),
    path('ticket/<str:ticket_type>/<int:ticket_id>/comment/<int:parent_id>/add', ticket_comment.Add.as_view(), name="_ticket_comment_problem_reply_add"),

    path("services", services.Index.as_view(), name="Services"),
    path("service/add", services.Add.as_view(), name="_service_add"),
    path("service/<int:pk>/edit", services.Change.as_view(), name="_service_change"),
    path("service/<int:pk>/delete", services.Delete.as_view(), name="_service_delete"),
    path("service/<int:pk>", services.View.as_view(), name="_service_view"),

]

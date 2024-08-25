from django.urls import path

from assistance.views import knowledge_base

from core.views import ticket, ticket_comment

app_name = "Assistance"

urlpatterns = [

    path("information", knowledge_base.Index.as_view(), name="Knowledge Base"),
    path("information/add", knowledge_base.Add.as_view(), name="_knowledge_base_add"),
    path("information/<int:pk>/edit", knowledge_base.Change.as_view(), name="_knowledge_base_change"),
    path("information/<int:pk>/delete", knowledge_base.Delete.as_view(), name="_knowledge_base_delete"),
    path("information/<int:pk>", knowledge_base.View.as_view(), name="_knowledge_base_view"),

    path('ticket/request', ticket.Index.as_view(), kwargs={'ticket_type': 'request'}, name="Requests"),
    path('ticket/<str:ticket_type>/add', ticket.Add.as_view(), name="_ticket_request_add"),
    path('ticket/<str:ticket_type>/<int:pk>/edit', ticket.Change.as_view(), name="_ticket_request_change"),
    path('ticket/<str:ticket_type>/<int:pk>', ticket.View.as_view(), name="_ticket_request_view"),

    path('ticket/<str:ticket_type>/<int:ticket_id>/comment/add', ticket_comment.Add.as_view(), name="_ticket_comment_request_add"),
    path('ticket/<str:ticket_type>/<int:ticket_id>/comment/<int:pk>/edit', ticket_comment.Change.as_view(), name="_ticket_comment_request_change"),
    path('ticket/<str:ticket_type>/<int:ticket_id>/comment/<int:parent_id>/add', ticket_comment.Add.as_view(), name="_ticket_comment_request_reply_add"),

]

import markdown

from django.views import generic

from access.mixin import OrganizationPermission

from django_celery_results.models import TaskResult



class Index(OrganizationPermission, generic.ListView):

    context_object_name = "task_results"

    fields = [
        "task_id",
        'task_name',
        'status',
        'date_created',
        'date_done',
    ]

    model = TaskResult

    permission_required = [
        'django_celery_results.view_taskresult',
    ]

    template_name = 'celery_log_index.html.j2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Background Task Results'

        return context


    def get_success_url(self, **kwargs):

        return reverse('Settings:_device_model_view', args=(self.kwargs['pk'],))



class View(OrganizationPermission, generic.UpdateView):

    context_object_name = "task_result"

    fields = [
        "task_id",
        'task_name',
        'status',
        'task_args',
    ]

    model = TaskResult

    permission_required = [
        'django_celery_results.view_taskresult',
    ]

    template_name = 'celery_log.html.j2'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = f"Task {self.object.task_id}"

        return context


    def post(self, request, *args, **kwargs):
        pass

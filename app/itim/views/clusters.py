from django.contrib.auth import decorators as auth_decorator
from django.urls import reverse
from django.utils.decorators import method_decorator

from core.forms.comment import AddNoteForm
from core.models.notes import Notes
from core.views.common import AddView, ChangeView, DeleteView, IndexView

from itim.forms.clusters import ClusterForm, DetailForm
from itim.models.clusters import Cluster
from itim.models.services import Service

from settings.models.user_settings import UserSettings



class Add(AddView):

    form_class = ClusterForm

    model = Cluster

    permission_required = [
        'itim.add_cluster',
    ]


    def get_initial(self):

        initial: dict = {
            'organization': UserSettings.objects.get(user = self.request.user).default_organization
        }

        if 'pk' in self.kwargs:

            if self.kwargs['pk']:

                initial.update({'parent': self.kwargs['pk']})

                self.model.parent.field.hidden = True

        return initial


    def get_success_url(self, **kwargs):

        return reverse('ITIM:Clusters')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'New Cluster'

        return context



class Change(ChangeView):

    form_class = ClusterForm

    model = Cluster

    permission_required = [
        'itim.change_cluster',
    ]


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['content_title'] = str(self.object)

        return context


    def get_success_url(self, **kwargs):

        return reverse('ITIM:_cluster_view', args=(self.kwargs['pk'],))



class Delete(DeleteView):

    model = Cluster

    permission_required = [
        'itim.delete_cluster',
    ]


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete ' + str(self.object)

        return context


    def get_success_url(self, **kwargs):

        return reverse('ITIM:Clusters')



class Index(IndexView):

    context_object_name = "items"

    model = Cluster

    paginate_by = 10

    permission_required = [
        'itim.view_cluster'
    ]

    template_name = 'itim/cluster_index.html.j2'


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['model_docs_path'] = self.model._meta.app_label + '/' + self.model._meta.model_name

        context['content_title'] = 'Clusters'

        return context



class View(ChangeView):

    context_object_name = "cluster"

    form_class = DetailForm

    model = Cluster

    permission_required = [
        'itim.view_cluster',
    ]

    template_name = 'itim/cluster.html.j2'


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['notes_form'] = AddNoteForm(prefix='note')
        context['notes'] = Notes.objects.filter(service=self.kwargs['pk'])

        context['model_pk'] = self.kwargs['pk']
        context['model_name'] = self.model._meta.model_name

        context['model_delete_url'] = reverse('ITIM:_cluster_delete', args=(self.kwargs['pk'],))

        context['services'] = Service.objects.filter(
            cluster = self.kwargs['pk']
        )


        context['content_title'] = self.object.name

        return context


    def post(self, request, *args, **kwargs):

        item = Cluster.objects.get(pk=self.kwargs['pk'])

        notes = AddNoteForm(request.POST, prefix='note')

        if notes.is_bound and notes.is_valid() and notes.instance.note != '':

            notes.instance.service = item

            notes.instance.organization = item.organization

            notes.save()


    def get_success_url(self, **kwargs):

        return reverse('ITIM:_cluster_view', args=(self.kwargs['pk'],))

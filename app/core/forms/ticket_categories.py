from django import forms
from django.forms import ValidationError
from django.urls import reverse

from app import settings

from core.forms.common import CommonModelForm
from core.models.ticket.ticket_category import TicketCategory



class TicketCategoryForm(CommonModelForm):


    class Meta:

        fields = '__all__'

        model = TicketCategory

    prefix = 'ticket_category'

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['parent'].queryset = self.fields['parent'].queryset.exclude(
            id=self.instance.pk
        )


    def clean(self):
        
        cleaned_data = super().clean()

        pk = self.instance.id

        parent = cleaned_data.get("parent")

        if pk:

            if parent == pk:

                raise ValidationError("Category can't have itself as its parent category")

        return cleaned_data



class DetailForm(TicketCategoryForm):


    tabs: dict = {
        "details": {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'parent',
                        'name',
                        'runbook',
                        'organization',
                        'c_created',
                        'c_modified'
                    ],
                    "right": [
                        'model_notes',
                    ]
                },
                {
                    "layout": "double",
                    "name": "Ticket Types",
                    "left": [
                        'change',
                        'problem',
                        'request'
                    ],
                    "right": [
                        'incident',
                        'project_task'
                    ]
                },
            ]
        },
        "notes": {
            "name": "Notes",
            "slug": "notes",
            "sections": []
        }
    }


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


        self.fields['c_created'] = forms.DateTimeField(
            label = 'Created',
            input_formats=settings.DATETIME_FORMAT,
            disabled = True,
            initial = self.instance.created,
        )

        self.fields['c_modified'] = forms.DateTimeField(
            label = 'Modified',
            input_formats=settings.DATETIME_FORMAT,
            disabled = True,
            initial = self.instance.modified,
        )


        self.tabs['details'].update({
            "edit_url": reverse('Settings:_ticket_category_change', kwargs={'pk': self.instance.pk})
        })

        self.url_index_view = reverse('Settings:_ticket_categories')


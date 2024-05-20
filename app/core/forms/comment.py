from django import forms

from app import settings
from core.models.notes import Notes


class AddNoteForm(forms.ModelForm):

    prefix = 'note'

    class Meta:
        model = Notes
        fields = [
            'note'
        ]

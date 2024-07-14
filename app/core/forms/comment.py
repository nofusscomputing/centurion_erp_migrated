from app import settings

from core.forms.common import CommonModelForm
from core.models.notes import Notes


class AddNoteForm(CommonModelForm):

    prefix = 'note'

    class Meta:
        model = Notes
        fields = [
            'note'
        ]

from django.db.models import Q

from core.forms.common import CommonModelForm

from itam.models.software import SoftwareCategory



class SoftwareCategoryForm(CommonModelForm):

    class Meta:

       fields = [
        'name',
        'slug',
        'id',
        'organization',
        'is_global',
        'model_notes',
       ]

       model = SoftwareCategory

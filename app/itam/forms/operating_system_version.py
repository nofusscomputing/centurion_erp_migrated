from django.db.models import Q

from core.forms.common import CommonModelForm

from itam.models.operating_system import OperatingSystemVersion



class OperatingSystemVersionForm(CommonModelForm):

    class Meta:

       fields = [
        'name',
       ]

       model = OperatingSystemVersion

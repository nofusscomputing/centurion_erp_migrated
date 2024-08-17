from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter()
@stringfilter
def choice_ids(value):
    """Convert choice field value to list
    
    Provide from `{{ field.field.choices }}` the `field.value` and have it converted to a loop

    Args:
        value (string): for field that has `field.field.choices`, provide `field.value`

    Returns:
        list: `field.value` casted to a useable list
    """

    if value == 'None':

        return ''

    alist: list = []

    if '[' in value:

        value = str(value).replace('[', '').replace(']', '')

        if ',' in value:

            for item in value.split(','):

                try:

                    alist += [ int(item) ]

                except:

                    alist += [ str(item) ]

        else:

            try:

                alist += [ int(item) ]

            except:

                alist += [ str(item) ]

    else:

        try:

            alist += [ int(value) ]

        except:

            alist += [ str(value) ]

    return alist
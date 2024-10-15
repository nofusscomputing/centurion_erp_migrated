from django.db import models
from django.utils.timezone import now
from django.template.defaultfilters import slugify

class AutoCreatedField(models.DateTimeField):
    """
    A DateTimeField that automatically populates itself at
    object creation.

    By default, sets editable=False, default=datetime.now.

    """

    help_text = 'Date and time of creation'

    verbose_name = 'Created'

    def __init__(self, *args, **kwargs):

        kwargs.setdefault("editable", False)

        kwargs.setdefault("default", now)

        kwargs.setdefault("help_text", self.help_text)

        kwargs.setdefault("verbose_name", self.verbose_name)

        super().__init__(*args, **kwargs)


class AutoLastModifiedField(AutoCreatedField):
    """
    A DateTimeField that updates itself on each save() of the model.

    By default, sets editable=False and default=datetime.now.

    """

    help_text = 'Date and time of last modification'

    verbose_name = 'Modified'

    def __init__(self, *args, **kwargs):

        kwargs.setdefault("help_text", self.help_text)

        kwargs.setdefault("verbose_name", self.verbose_name)

        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):

        value = now()

        setattr(model_instance, self.attname, value)

        return value


class AutoSlugField(models.SlugField):
    """
    A DateTimeField that updates itself on each save() of the model.

    By default, sets editable=False and default=datetime.now.

    """

    help_text = 'slug for this field'

    verbose_name = 'Slug'


    def __init__(self, *args, **kwargs):

        kwargs.setdefault("help_text", self.help_text)

        kwargs.setdefault("verbose_name", self.verbose_name)

        super().__init__(*args, **kwargs)


    def pre_save(self, model_instance, add):

        if not model_instance.slug or model_instance.slug == '_':
            value = model_instance.name.lower().replace(' ', '_')

            setattr(model_instance, self.attname, value)

            return value

        return model_instance.slug



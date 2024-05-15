from django.db import models
from django.utils.timezone import now
from django.template.defaultfilters import slugify

class AutoCreatedField(models.DateTimeField):
    """
    A DateTimeField that automatically populates itself at
    object creation.

    By default, sets editable=False, default=datetime.now.

    """

    def __init__(self, *args, **kwargs):

        kwargs.setdefault("editable", False)

        kwargs.setdefault("default", now)

        super().__init__(*args, **kwargs)


class AutoLastModifiedField(AutoCreatedField):
    """
    A DateTimeField that updates itself on each save() of the model.

    By default, sets editable=False and default=datetime.now.

    """

    def pre_save(self, model_instance, add):

        value = now()

        setattr(model_instance, self.attname, value)

        return value


class AutoSlugField(models.SlugField):
    """
    A DateTimeField that updates itself on each save() of the model.

    By default, sets editable=False and default=datetime.now.

    """

    def pre_save(self, model_instance, add):

        if not model_instance.slug or model_instance.slug == '_':
            value = model_instance.name.lower().replace(' ', '_')

            setattr(model_instance, self.attname, value)

            return value

        return model_instance.slug



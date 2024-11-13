from rest_framework import serializers

from core.fields import CharField



class MarkdownField(CharField):


    style_class: str = None
    """ UI field Additional CSS classes

    Format for this value is Sapce Seperated Value (SSV)
    """

    def __init__(
        self,
        multiline = True,
        style_class = None,
        **kwargs
    ):

        self.style_class = style_class

        super().__init__(multiline = multiline, **kwargs)

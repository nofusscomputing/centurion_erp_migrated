from rest_framework import serializers

from core.fields import CharField



class MarkdownField(CharField):

    def __init__(self, multiline = True, **kwargs):

        super().__init__(multiline = multiline, **kwargs)

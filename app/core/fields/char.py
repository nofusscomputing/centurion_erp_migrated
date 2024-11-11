from rest_framework import serializers



class CharField(serializers.CharField):

    source = ''

    label = ''

    textarea: bool


    def __init__(self, multiline = False, **kwargs):

        self.textarea = multiline

        super().__init__(**kwargs)

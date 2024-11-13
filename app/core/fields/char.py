from rest_framework import serializers



class CharField(serializers.CharField):

    autolink: bool = False

    source = ''

    label = ''

    textarea: bool


    def __init__(
        self,
        autolink = False,
        multiline = False,
        **kwargs
    ):

        self.autolink = autolink

        self.textarea = multiline

        super().__init__(**kwargs)

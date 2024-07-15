from django import forms



class CommonModelForm(forms.ModelForm):
    """ Abstract Form class for form inclusion

    This class exists so that common functions can be conducted against forms as they are loaded.
    """


    def __init__(self, *args, **kwargs):
        """Form initialization.

        Initialize the form using the super classes first then continue to initialize the form using logic
        contained within this method.


        !!! danger "Requirement"
            This method may be overridden however must still be called from the overriding function. i.e. `super().__init__(*args, **kwargs)`
        """

        super().__init__(*args, **kwargs)

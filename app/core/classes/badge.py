from core.classes.icon import Icon



class Badge:

    icon: Icon

    text: str

    text_style:str

    url:str


    def __init__(self, 
        icon_name: str = None,
        icon_style: str = None,
        text: str = None,
        text_style: str = None,
        url: str = None
    ):

        self.icon = Icon(
            name=icon_name,
            style = icon_style
        )

        self.text = text

        self.text_style = text_style

        self.url = url


    @property
    def to_json(self):

        return {
            'icon': self.icon.to_json,
            'text': self.text,
            'text_style': self.text_style,
            'url': self.url,
        }

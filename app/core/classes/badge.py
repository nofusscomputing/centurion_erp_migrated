


class Badge:

    icon: str

    icon_style:str

    text: str

    text_style:str

    url:str


    def __init__(self, 
        icon: str = None,
        icon_style: str = None,
        text: str = None,
        text_style: str = None,
        url: str = None
    ):

        self.icon = icon

        self.icon_style = icon_style

        self.text = text

        self.text_style = text_style

        self.url = url

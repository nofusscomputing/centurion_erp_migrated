


class Icon:

    name: str

    style:str


    def __init__(self, 
        name: str = None,
        style: str = None,
        url: str = None
    ):

        self.name = name

        self.style = style

        self.url = url

    @property
    def to_json(self):

        return {
            'name': self.name,
            'style': self.style
        }

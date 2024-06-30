from django.core.exceptions import ValidationError
from django.utils.html import escape

class Inventory:
    """ Inventory Object

    Pass in an Inventory dict that a device has provided and sanitize ready for use.

    Raises:
        ValidationError: Malformed inventory data.
    """


    class Details:

        _name: str

        _serial_number: str

        _uuid: str


        def __init__(self, details: dict):

            self._name = escape(details['name'])

            self._serial_number = escape(details['serial_number'])

            self._uuid = escape(details['uuid'])


        @property
        def name(self) -> str:

            return str(self._name)


        @property
        def serial_number(self) -> str:

            return str(self._serial_number)


        @property
        def uuid(self) -> str:

            return str(self._uuid)



    class OperatingSystem:

        _name: str

        _version_major: str

        _version: str


        def __init__(self, operating_system: dict):

            self._name = escape(operating_system['name'])

            self._version_major = escape(operating_system['version_major'])

            self._version = escape(operating_system['version'])


        @property
        def name(self) -> str:

            return str(self._name)


        @property
        def version_major(self) -> str:

            return str(self._version_major)


        @property
        def version(self) -> str:

            return str(self._version)



    class Software:

        _name: str

        _category: str

        _version: str


        def __init__(self, software: dict):

            self._name = escape(software['name'])

            self._category = escape(software['category'])

            self._version = escape(software['version'])


        @property
        def name(self) -> str:

            return str(self._name)


        @property
        def category(self) -> str:

            return str(self._category)


        @property
        def version(self) -> str:

            return str(self._version)



    _details: Details = None

    _operating_system: OperatingSystem = None

    _software: list[Software] = []


    def __init__(self, inventory: dict):

        if (
            type(inventory['details']) is dict and
            type(inventory['os']) is dict and
            type(inventory['software']) is list
        ):

            self._details = self.Details(inventory['details'])

            self._operating_system = self.OperatingSystem(inventory['os'])

            for software in inventory['software']:

                self._software += [ self.Software(software) ]

        else:

            raise ValidationError('Inventory File is invalid')


    @property
    def details(self) -> Details:

        return self._details


    @property
    def operating_system(self) -> OperatingSystem:

        return self._operating_system


    @property
    def software(self) -> list[Software]:

        return list(self._software)

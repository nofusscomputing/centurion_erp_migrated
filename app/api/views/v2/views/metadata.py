from rest_framework_json_api.metadata import JSONAPIMetadata
from rest_framework.reverse import reverse


class NavigationMetadata(JSONAPIMetadata):


    def determine_metadata(self, request, view):

        metadata = super().determine_metadata(request, view)

        metadata['navigation'] = [
            {
                "name": "ITAM",
                "pages": [
                    {
                        "name": "Devices",
                        "icon": "device",
                        "link": "/itam/device"
                    }
                ]
            }
        ]

        return metadata

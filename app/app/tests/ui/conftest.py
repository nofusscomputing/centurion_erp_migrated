from app.urls import urlpatterns

class Data:


    def parse_urls(self, patterns, parent_route = None) -> list:

        urls = []

        root_paths = [
            'access',
            # 'account',
            # 'api',
            'config_management',
            'history',
            'itam',
            'organization',
            'settings'
        ]

        for url in patterns:

            if hasattr(url, 'pattern'):

                route = None

                if hasattr(url.pattern, '_route'):

                    if parent_route:

                        route = parent_route + url.pattern._route

                        route = str(route).replace('<int:device_id>', '1')
                        route = str(route).replace('<int:group_id>', '1')
                        route = str(route).replace('<int:operating_system_id>', '1')
                        route = str(route).replace('<int:organization_id>', '1')
                        route = str(route).replace('<int:pk>', '1')
                        route = str(route).replace('<int:software_id>', '1')
                        route = str(route).replace('<int:team_id>', '1')

                        if route != '' and route not in urls:

                            urls += [ route ]

                    else:

                        route = url.pattern._route

                        route = str(route).replace('<int:device_id>', '1')
                        route = str(route).replace('<int:group_id>', '1')
                        route = str(route).replace('<int:operating_system_id>', '1')
                        route = str(route).replace('<int:organization_id>', '1')
                        route = str(route).replace('<int:pk>', '1')
                        route = str(route).replace('<int:software_id>', '1')
                        route = str(route).replace('<int:team_id>', '1')

                        if str(url.pattern._route).replace('/', '') in root_paths:
                            
                            if route != '' and route not in urls:

                                urls += [ route ]

                if hasattr(url, 'url_patterns'):

                    if str(url.pattern._route).replace('/', '') in root_paths:

                        urls += self.parse_urls(patterns=url.url_patterns, parent_route=url.pattern._route)

        return urls


    def __init__(self):

        urls = []

        patterns = urlpatterns

        urls_found = self.parse_urls(patterns=patterns)

        for url in urls_found:

            if url not in urls:

                urls += [ url ]

        self.urls = urls

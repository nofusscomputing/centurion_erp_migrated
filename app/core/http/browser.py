import requests



class Browser:

    response: requests.Response = None

    @property
    def status() -> int:
        """ HTTP Status Code

        Returns:
            int: Return the HTTP status code from the last request
        """
        return self.response.status_code


    def get(
        self,
        url: str,
        headers: dict = {},
        ssl_verify: bool = True
    ) -> requests.Response:
        """ Perform a HTTP/GET request

        Args:
            url (str): URL to fetch.
            headers (dict, optional): Request Headers. Defaults to {}.
            ssl_verify (bool, optional): Verify the SSL Certificate. Defaults to True.

        Returns:
            requests.Response: The requests response object
        """


        headers.update({
            "Accept": "application/json",
            "Authorization": "Bearer xx" # AWX auth
        })

        response = requests.get(
            headers = headers,
            timeout = 3,
            url = url,
            verify = ssl_verify,
        )

        if response.status_code == 200:

            self.response = response

        return self.response


    def post(
        self,
        url: str,
        headers: dict = {},
        data: dict = None,
        ssl_verify: bool = True
    ) -> requests.Response:
        """ Perform an HTTP/POST request

        Args:
            url (str): _description_
            headers (dict, optional): Request Headers. Defaults to {}.
            data (dict, optional): _description_. Defaults to None.
            ssl_verify (bool, optional): Verify the SSL Certificate. Defaults to True.

        Returns:
            requests.Response: _description_
        """

        response = request.post(
            headers={
                "Content-Type": "application/json"
            },
            timeout = 3,
            url = url,
            data = data,
            verify = ssl_verify,
        )

        if response.status_code == 200:
            
            self.response = response

        return self.response

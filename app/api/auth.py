import datetime

from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from api.models.tokens import AuthToken



class TokenAuthentication(BaseAuthentication):
    """ API Token Authentication

    Provides the ability to use the API by using a token to authenticate.
    """

    def authenticate_header(self, request):
        return 'Token'


    def authenticate(self, request):
        """ Authentication the API session using the supplied token

        Args:
            request (object): API Request Object

        Raises:
            exceptions.AuthenticationFailed: 'Token header invalid' - Authorization Header Value is not in format `Token <auth-token>`
            exceptions.AuthenticationFailed: 'Token header invalid. Possibly incorrectly formatted' - Authentication header value has >1 space
            exceptions.AuthenticationFailed: 'Invalid token header. Token string should not contain invalid characters.' - Authorization header contains non-unicode chars

        Returns:
            None (None): User not authenticated
            tuple(user,token): User authenticated
        """

        auth = get_authorization_header(request).split()

        if not auth:
            return None

        if len(auth) == 1:

            raise exceptions.AuthenticationFailed('Token header invalid')

        elif len(auth) > 2:

            raise exceptions.AuthenticationFailed('Token header invalid. Possibly incorrectly formatted')


        elif len(auth) == 2:

            try:

                decoded_token: str = auth[1].decode("utf-8")

                for token in AuthToken.objects.filter():

                    provided_token: str = token.token_hash(decoded_token)

                    if token.token == provided_token:

                        if datetime.datetime.strptime(str(token.expires),'%Y-%m-%d %H:%M:%S%z') > datetime.datetime.now(datetime.timezone.utc):

                            user = token.user

                            return (user, provided_token)

                        else:

                            expired_token = AuthToken.objects.get(id=token.id)
                            
                            expired_token.delete()

            except UnicodeError:

                raise exceptions.AuthenticationFailed('Invalid token header. Token string should not contain invalid characters.')


        return None

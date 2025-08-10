from azure.core.credentials import TokenCredential
from azure.core.credentials import AccessToken
import time

class MyTokenCredential(TokenCredential):
    def __init__(self, access_token, expires_on=None):
        self._access_token = access_token
        # expires_on should be a unix timestamp; default to 1 hour from now if not provided
        self._expires_on = expires_on or int(time.time()) + 3600

    def get_token(self, *scopes, **kwargs):
        return AccessToken(self._access_token, self._expires_on)
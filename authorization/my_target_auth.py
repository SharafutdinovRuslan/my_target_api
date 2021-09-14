import os
import requests
from abc import abstractmethod, ABC

from http_api_environment import HttpApiEnvironment


class MyTargetAuth(ABC):

    def __init__(self, api_environment: HttpApiEnvironment, client_id: str, client_secret: str):
        self._client_id = client_id
        self._client_secret = client_secret
        self.api_environment = api_environment

    def _get_url(self, *args):
        return os.path.join(self.api_environment.entrypoint, *args)

    @abstractmethod
    def get_access_token(self) -> requests.Response:
        pass

    @abstractmethod
    def refresh_access_token(self, refresh_token) -> requests.Response:
        pass

    @abstractmethod
    def delete_user_access_tokens(self) -> requests.Response:
        pass

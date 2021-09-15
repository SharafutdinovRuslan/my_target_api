import requests
import os

from http_api_environment import HttpApiEnvironment


class HttpExecutor:

    ALLOWED_HTTP_METHODS = ('get', 'post', 'delete')

    def __init__(self, access_token: str, api_environment: HttpApiEnvironment):
        self.access_token = access_token
        self.api_environment = api_environment

    def _get_url(self, *args):
        return os.path.join(self.api_environment.entrypoint, *args)

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        if method not in self.ALLOWED_HTTP_METHODS:
            raise ValueError(f'Method {method} is not allowed')

        url = self._get_url(path)
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            **kwargs.get('headers', {})
        }
        kwargs.pop('headers', None)

        return requests.request(method=method, url=url, headers=headers, **kwargs)

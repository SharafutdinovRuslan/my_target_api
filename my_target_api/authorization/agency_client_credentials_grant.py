import requests

from authorization.my_target_auth import MyTargetAuth
from http_api_environment import HttpApiEnvironment


class AgencyClientCredentialsGrant(MyTargetAuth):

    def __init__(self, api_environment: HttpApiEnvironment, client_id: str, client_secret: str, agency_client_name: str):
        super().__init__(api_environment, client_id, client_secret)
        self.agency_client_name = agency_client_name

    def get_access_token(self, is_permanent: bool = False) -> requests.Response:

        return requests.request(
            method='post',
            url=self._get_url('oauth2/token.json'),
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            data={
                'grant_type': 'agency_client_credentials',
                'client_id': self._client_id,
                'client_secret': self._client_secret,
                'agency_client_name': self.agency_client_name,
                'permanent': is_permanent
            }
        )

    def refresh_access_token(self, refresh_token) -> requests.Response:

        return requests.request(
            method='post',
            url=self._get_url('oauth2/token.json'),
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            data={
                'grant_type': 'refresh_token',
                'client_id': self._client_id,
                'client_secret': self._client_secret,
                'refresh_token': refresh_token
            }
        )

    def delete_user_access_tokens(self) -> requests.Response:

        return requests.request(
            method='post',
            url=self._get_url('oauth2/token/delete.json'),
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            data={
                'client_id': self._client_id,
                'client_secret': self._client_secret,
                'username': self.agency_client_name,
            }
        )

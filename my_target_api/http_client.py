from http import HTTPStatus

from http_api_environment import HttpApiEnvironment
from authorization.agency_client_credentials_grant import AgencyClientCredentialsGrant
from executors.http_executor import HttpExecutor
from exceptions.my_target_api_base_exception import MyTargetApiBaseException
from resources.remarketing_users_list import RemarketingUsersList
from resources.segments import Segments


class HttpClient:

    def __init__(self, client_id: str, client_secret: str, agency_client_name: str,
                 is_sandbox: bool = False, api_version: str = HttpApiEnvironment.DEFAULT_API_VERSION):
        self.client_id = client_id
        self.client_secret = client_secret
        self.agency_client_name = agency_client_name
        self.api_environment = HttpApiEnvironment(is_sandbox=is_sandbox, api_version=api_version)

        self._authorization_method = AgencyClientCredentialsGrant(
            self.api_environment, self.client_id, self.client_secret, self.agency_client_name
        )
        self._access_token = None
        self._refresh_token = None

    def initialize_access_token(self, access_token: str = None, refresh_token: str = None, is_permanent: bool = False):
        if access_token:
            self._access_token, self._refresh_token = access_token, refresh_token
        elif refresh_token and not access_token:
            raise ValueError('Access token should be set too!')
        else:
            self._access_token, self._refresh_token = self._get_access_token(is_permanent)

    def _get_access_token(self, is_permanent: bool = False) -> tuple:
        response = self._authorization_method.get_access_token(is_permanent)

        if response.status_code != HTTPStatus.OK:
            raise MyTargetApiBaseException(response)
        return response.json().get('access_token'), response.json().get('refresh_token')

    def _get_http_executor(self, api_version: str = HttpApiEnvironment.DEFAULT_API_VERSION) -> HttpExecutor:
        api_version = api_version or self.api_environment.api_version
        executor_api_environment = HttpApiEnvironment(self.api_environment.is_sandbox, api_version)

        return HttpExecutor(self._access_token, executor_api_environment)

    def get_remarketing_users_list(self) -> RemarketingUsersList:
        executor = self._get_http_executor(HttpApiEnvironment.API_VERSION_V3)

        return RemarketingUsersList(executor=executor)

    def upload_remarketing_users_list(self, file_path: str, list_name: str, list_type: str):
        remarketing_users_list = self.get_remarketing_users_list()

        response = remarketing_users_list.post(
            file_path, list_name, list_type
        )

        if response.status_code != HTTPStatus.OK:
            raise MyTargetApiBaseException(response)
        return response

    def get_segments(self) -> Segments:
        executor = self._get_http_executor(HttpApiEnvironment.API_VERSION_V2)

        return Segments(executor=executor)

    def create_segments(self, segment_name: str, pass_condition: int, relations: list, **kwargs):
        segments = self.get_segments()

        response = segments.post(
            segment_name, pass_condition, relations, **kwargs
        )

        if response.status_code != HTTPStatus.OK:
            raise MyTargetApiBaseException(response)
        return response



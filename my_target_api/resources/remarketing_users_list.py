import requests
from typing import Union

from resources.abstract_resource import AbstractResource
from executors.http_executor import HttpExecutor


class RemarketingUsersList(AbstractResource):

    ALLOWED_LIST_TYPES = ('ok', 'vk', 'dmp_id', 'idfa', 'advertising_id')

    def __init__(self, executor: HttpExecutor):
        super().__init__(executor)

    def post(self, file_path: str, list_name: str, list_type: str) -> requests.Response:
        if list_type not in self.ALLOWED_LIST_TYPES:
            raise ValueError(f'List type {list_type} is not allowed')

        return self.executor.request(
            method='post',
            path='remarketing/users_lists.json',
            data={
                'name': list_name,
                'type': list_type
            },
            files={
                'file': open(file_path, 'rb')
            }
        )

    def get(self, list_id: Union[int, str]):

        return self.executor.request(
            method='get',
            path=f'remarketing/users_lists/{list_id}.json',
            headers={
                'Content-Type': 'multipart/form-data',
            },
        )

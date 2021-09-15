import requests
from typing import Union

from resources.abstract_resource import AbstractResource
from executors.http_executor import HttpExecutor


class Segments(AbstractResource):

    def __init__(self, executor: HttpExecutor):
        super().__init__(executor)

    def post(self, segment_name: str, pass_condition: int, relations: list, **kwargs) -> requests.Response:

        required_json = {
            'name': segment_name,
            'pass_condition': pass_condition,
            'relations': relations,
        }

        return self.executor.request(
            method='post',
            path='remarketing/segments.json',
            json={**required_json, **kwargs}
        )

    def get(self, segment_id: Union[int, str]):

        return self.executor.request(
            method='get',
            path=f'remarketing/segments/{segment_id}.json',
        )

    def delete(self, segment_id):

        return self.executor.request(
            method='delete',
            path=f'remarketing/segments/{segment_id}.json',
        )

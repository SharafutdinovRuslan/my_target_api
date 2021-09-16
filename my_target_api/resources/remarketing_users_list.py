import requests
from typing import Union, List

from resources.abstract_resource import AbstractResource
from executors.http_executor import HttpExecutor


class RemarketingUsersList(AbstractResource):

    USER_LIST_MAX_CHUNK_SIZE = 4999999
    USER_LIST_MIN_CHUNK_SIZE = 1999

    ALLOWED_LIST_TYPES = ('ok', 'vk', 'dmp_id', 'idfa', 'advertising_id')

    def __init__(self, executor: HttpExecutor):
        super().__init__(executor)

    @staticmethod
    def add_user_list_headers(user_list: List[Union[str]], list_type: str, partner_id: int = None) -> str:
        if list_type == 'dmp_id':
            if not partner_id:
                raise KeyError('for dmp_id list type partner_id should be set to')
            header = f'{partner_id},\nid,\n'
        else:
            header = 'id,\n'

        ids = list(map(str, user_list))

        return header + '\n'.join(ids)

    @staticmethod
    def split_user_list_by_chunks(user_list: List[Union[str, int]], list_type: str):
        max_chunk_size, min_chink_size = (RemarketingUsersList.USER_LIST_MAX_CHUNK_SIZE, RemarketingUsersList.USER_LIST_MIN_CHUNK_SIZE) if list_type != 'dmp_id' \
            else (RemarketingUsersList.USER_LIST_MAX_CHUNK_SIZE - 1, RemarketingUsersList.USER_LIST_MIN_CHUNK_SIZE - 1)

        if len(user_list) < min_chink_size:
            return user_list

        chunks = []
        chunk = []
        for user_id in user_list:
            if len(chunk) < max_chunk_size:
                chunk.append(user_id)
            else:
                chunks.append(chunk)
                chunk = [user_id]

        if len(chunk) < min_chink_size and len(chunks) > 0:
            chunk.extend(chunks[-1][len(chunks[-1]) // 2:])
            chunks[-1] = chunks[-1][:len(chunks[-1]) // 2]
            chunks.append(chunk)
        else:
            chunks.append(chunk)

        return chunks

    def post(self, user_list: List[Union[str, int]], list_name: str, list_type: str, list_id: int = None, partner_id: int = None) -> requests.Response:
        if list_type not in self.ALLOWED_LIST_TYPES:
            raise ValueError(f'List type {list_type} is not allowed')

        data = {
            'name': list_name,
            'type': list_type,
            **({'base': list_id} if list_id else {})
        }

        prepared_user_list = self.add_user_list_headers(user_list, list_type, partner_id)
        return self.executor.request(
            method='post',
            path='remarketing/users_lists.json',
            data=data,
            files={
                'file': ('file.csv', prepared_user_list)
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

    def delete(self, list_id: Union[int, str]):

        return self.executor.request(
            method='delete',
            path=f'remarketing/users_lists/{list_id}.json',
            headers={
                'Content-Type': 'multipart/form-data',
            },
        )

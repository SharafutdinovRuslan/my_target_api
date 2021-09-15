# MyTarget API Wrappers

## Установка
```shell
python -m pip install git+https://github.com/SharafutdinovRuslan/my_target_api
```

## Примеры использования: 
```python
from my_target_api.http_client import HttpClient
import os


client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
agency_client_name = os.environ.get('AGENCY_CLIENT_NAME')

client = HttpClient(
    client_id, client_secret, agency_client_name, is_sandbox=True,
)
client.initialize_access_token(is_permanent=False)

upload_remarketing_users_list_response = client.upload_remarketing_users_list(
    file_path='/your/file/path/ok.csv',
    list_name='тестовый список ОК',
    list_type='ok',
)


response_create_segment = client.create_segments(
    segment_name='тестовый сегмент',
    pass_condition=1,
    relations=[
            {
                "object_type": "remarketing_users_list",
                "object_id": 123456,
                "params": {
                    "type": "positive",
                    "source_id": 123456,
                }
            },
        ]
)

```

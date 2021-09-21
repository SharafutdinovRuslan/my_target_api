import os


class HttpApiEnvironment:

    HTTP_ENTRYPOINT_SANDBOX = 'https://target-sandbox.my.com/api/'
    HTTP_ENTRYPOINT = 'https://target.my.com/api/'

    API_VERSION_V2 = 'v2'
    API_VERSION_V3 = 'v3'
    DEFAULT_API_VERSION = API_VERSION_V2

    def __init__(self, is_sandbox: bool, api_version: str = DEFAULT_API_VERSION):
        self.is_sandbox = is_sandbox
        self.api_version = api_version
        self.entrypoint = os.path.join(
            self.HTTP_ENTRYPOINT_SANDBOX if is_sandbox else self.HTTP_ENTRYPOINT,
            api_version
        )

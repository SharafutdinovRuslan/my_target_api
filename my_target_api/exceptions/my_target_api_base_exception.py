from requests import Response


class MyTargetApiBaseException(Exception):

    def __init__(self, response: Response):
        self.response = response

    def __str__(self):
        return f"""
        HEADERS: {str(self.response.headers)}
        URL: {self.response.url}
        STATUS CODE: {self.response.status_code}
        REASON: {self.response.reason}
        TEXT: {self.response.text}
        """

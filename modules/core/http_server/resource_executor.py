from modules.core.http_server.base_executor import BaseExecutor
from modules.core.http_server.http_request import Http_Request
from modules.core.http_server.http_response import Http_Response


class ResourceExecutor(BaseExecutor):
    def __init__(self, file: str):
        self.file = file

    def generate(self, req: Http_Request) -> Http_Response:
        file = open(self.file, 'rb') # open file , r => read , b => byte format
        response = file.read()
        file.close()
        body = response

        headers = [
            ('Content-Length', len(body)),
            ('Access-Control-Allow-Origin', '*'),
            ("Access-Control-Allow-Credentials", "true"),
            ("Access-Control-Allow-Methods", "GET,HEAD,OPTIONS,POST,PUT"),
            ("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization, Special-Request-Header, get_month_times"),
        ]

        return Http_Response(200, 'OK', headers, body)

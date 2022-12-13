import json

from modules.core.http_server.http_error import Http_Error
from modules.core.http_server.http_request import Http_Request
from modules.core.http_server.http_response import Http_Response
from web_host.messages.base_response import BaseResponse


class BaseExecutor:
    def execute(self, req: Http_Request) -> Http_Response:
        raise Exception('Not implemented')

    def generate_success(self, contentType: str, body: BaseResponse) -> Http_Response:
        rawData = f'{json.dumps(body.toJson())}'.encode('utf-8')
        headers = [
            ('Content-Type', contentType),
            ('Content-Length', len(rawData)),
            ('Access-Control-Allow-Origin', '*'),
        ]
        return Http_Response(200, 'Ok', headers=headers, body=rawData)

    def generate_failed(self, body: str) -> Http_Response:
        rawData = f'{body}'.encode('utf-8')
        return Http_Error(510, 'Internal exceptiom', body=rawData)

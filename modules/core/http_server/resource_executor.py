import os

from jinja2 import FileSystemLoader, Environment

from modules.core.http_server.core_http_server import CoreHttpServer
from modules.core.http_server.http_error import Http_Error
from modules.core.http_server.http_request import Http_Request
from modules.core.http_server.http_response import Http_Response


class ResourceExecutor:
    def __init__(self, file: str):
        self.file = file

    def generate(self, req: Http_Request) -> Http_Response:
        file = open(self.file, 'rb') # open file , r => read , b => byte format
        response = file.read()
        file.close()
        body = response
        headers = [('Content-Length', len(body))]
        return Http_Response(200, 'OK', headers, body)

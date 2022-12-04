import os

from jinja2 import FileSystemLoader, Environment

from modules.core.http_server.core_http_server import CoreHttpServer
from modules.core.http_server.http_error import Http_Error
from modules.core.http_server.http_request import Http_Request
from modules.core.http_server.http_response import Http_Response


class TemplatePageExecutor:
    def __init__(self, template_folder: str, file: str, params: {str, object}):
        self.params = params
        self.file = file
        self.template_folder = template_folder

    def generate(self, req: Http_Request) -> Http_Response:
        contentType = 'text/html; charset=utf-8'
        templateLoader = FileSystemLoader(searchpath=self.template_folder)
        templateEnv = Environment(loader=templateLoader)
        template = templateEnv.get_template(self.file)
        body = template.render(self.params)
        body = body.encode('utf-8')
        headers = [('Content-Type', contentType),
                   ('Content-Length', len(body))]
        return Http_Response(200, 'OK', headers, body)

import json
from jinja2 import Template, FileSystemLoader, Environment

from modules.logger_viewer.log_service import Log_Service
from modules.logger_viewer.models.http_request import Http_Request
from modules.logger_viewer.models.http_response import Http_Response


class Default_Page_Generator:
    def __init__(self, log_service: Log_Service, template_folder: str):
        self.template_folder = template_folder
        self.log_service = log_service

    def generate(self, req: Http_Request):
        accept = req.headers.get('Accept')
        applications = self.log_service.get_applications()
        if 'text/html' in accept:
            contentType = 'text/html; charset=utf-8'
            templateLoader = FileSystemLoader(searchpath=self.template_folder)
            templateEnv = Environment(loader=templateLoader)
            TEMPLATE_FILE = "main_page.html"
            template = templateEnv.get_template(TEMPLATE_FILE)
            body = template.render(results=applications)

        # elif 'application/json' in accept:
        #     contentType = 'application/json; charset=utf-8'
        #     # body = json.dumps(self._users)

        else:
            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/406
            return Http_Response(406, 'Not Acceptable')

        body = body.encode('utf-8')
        headers = [('Content-Type', contentType),
                   ('Content-Length', len(body))]
        return Http_Response(200, 'OK', headers, body)
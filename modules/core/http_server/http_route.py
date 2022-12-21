from modules.core.http_server.base_executor import BaseExecutor
from modules.core.http_server.http_method import HTTPMethod


class HttpRoute:
    def __init__(self, method: HTTPMethod, path: str, callback: BaseExecutor):
        self.method = method
        self.callback = callback
        self.path = path

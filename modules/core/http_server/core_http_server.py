import os

from aiohttp import web
from aiohttp.web_routedef import RouteDef

from modules.core.http_server.http_method import HTTPMethod
from modules.core.http_server.http_route import HttpRoute
from modules.core.http_server.resource_executor import ResourceExecutor


class AiohttpHttpServer:
    def __init__(self, port, host='0.0.0.0'):
        self._host = host
        self._port = port
        self.app = web.Application()

    def add_static(self, path_to_static_folder: str, react_routers: list[str]):
        main_page = "index.html"
        routes: [RouteDef] = []

        for dp, dn, filenames in os.walk(path_to_static_folder):
            for f in filenames:
                full_path = os.path.join(dp, f)
                html_path = full_path.replace(path_to_static_folder, str())
                html_path = html_path.replace('\\', '/')
                if f == main_page:
                    for react_route in react_routers:
                        routes.append(web.get(react_route, ResourceExecutor(full_path).execute))
                    continue
                routes.append(web.get(html_path, ResourceExecutor(full_path).execute))

        self.app.add_routes(routes)

    def add_get_handler(self, handlers: list[HttpRoute]):
        routes: [RouteDef] = []
        for handler in handlers:
            if handler.method == HTTPMethod.GET:
                routes.append(web.get(handler.path, handler.callback.execute))
            if handler.method == HTTPMethod.PUT:
                routes.append(web.put(handler.path, handler.callback.execute))

        self.app.add_routes(routes)

    def serve_forever(self):
        web.run_app(self.app, port=self._port, host=self._host)

import json
import os
from typing import Dict

from jsonpath_rw import parse

from keenetic_prometheus_exporter.http_callbacks.metrics_request_executor import GetMetricsRequestExecutor
from models.keenetic_api import KeeneticClient
from models.keenetic_collecor import KeeneticCollector
from modules.core.http_server.core_http_server import AiohttpHttpServer
from modules.core.http_server.http_method import HTTPMethod
from modules.core.http_server.http_route import HttpRoute

ADMIN_ENDPOINT = 'KEENETIC_ADMIN_ENDPOINT'
LOGIN = 'KEENETIC_ADMIN_USERNAME'
PASSWORD = 'KEENETIC_ADMIN_PASSWORD'
CONFIG_PATH = 'CONFIG_PATH'
METRICS_API = "/metrics"
# Documentation
# https://storage.googleapis.com/docs.help.keenetic.com/cli/3.9/ru/cli_manual_kn-1810_ru.pdf


def json_path_init(paths: Dict[str, str]):
    queries = {}

    for pathName, path in paths.items():
        if path == "~":
            queries[pathName] = path
        else:
            queries[pathName] = parse(path)

    return queries


if __name__ == '__main__':
    pwd = os.path.dirname(os.path.realpath(__file__))
    admin_endpoint = os.environ[ADMIN_ENDPOINT]
    login = os.environ[LOGIN]
    password = os.environ[PASSWORD]
    config_path = os.environ[CONFIG_PATH]

    metrics_configuration = json.load(open(config_path, "r"))

    collectors = []
    keeneticClient = KeeneticClient(admin_endpoint, login, password)

    for metric_configuration in metrics_configuration['metrics']:

        _command: str = metric_configuration['command']
        if _command != 'ntce hosts':
            continue
        _params = metric_configuration.get('param', {})
        _root = parse(metric_configuration['root'])
        _tags = json_path_init(metric_configuration['tags'])
        _values = json_path_init(metric_configuration['values'])

        collectors.append(KeeneticCollector(_command, _params, _root, _tags, _values))

    aiohHttpServer = AiohttpHttpServer(6789)
    aiohHttpServer.add_get_handler([HttpRoute(HTTPMethod.GET, f'{METRICS_API}', GetMetricsRequestExecutor(keeneticClient, collectors))])

    aiohHttpServer.serve_forever()

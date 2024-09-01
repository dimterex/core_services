import json
import os
from typing import Dict

from jsonpath_rw import parse

from core.log_service.log_service import Logger_Service
from core.rabbitmq.messages.configuration.tokens.get_token_request import GetTokenRequest
from core.rabbitmq.messages.configuration.urls.get_url_request import GetUrlRequest
from core.rabbitmq.messages.identificators import CONFIGURATION_QUEUE, KEENETIC_ADMIN_ENDPOINT, KEENETIC_ADMIN_USERNAME, \
    KEENETIC_ADMIN_PASSWORD
from core.rabbitmq.messages.status_response import ERROR_STATUS_CODE
from core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from keenetic_prometheus_exporter.http_callbacks.metrics_request_executor import GetMetricsRequestExecutor
from models.keenetic_api import KeeneticClient
from models.keenetic_collecor import KeeneticCollector
from core.http_server.core_http_server import AiohttpHttpServer
from core.http_server.http_method import HTTPMethod
from core.http_server.http_route import HttpRoute

RABBIT_CONNECTION_STRING = 'RABBIT_AMPQ_URL'
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

    ampq_url = os.environ[RABBIT_CONNECTION_STRING]
    logger_service = Logger_Service()

    rpc_publisher = RpcPublisher(ampq_url)
    admin_endpoint_response = rpc_publisher.call(CONFIGURATION_QUEUE, GetUrlRequest(KEENETIC_ADMIN_ENDPOINT))
    if admin_endpoint_response.status == ERROR_STATUS_CODE:
        raise Exception(admin_endpoint_response.message)

    login_response = rpc_publisher.call(CONFIGURATION_QUEUE, GetTokenRequest(KEENETIC_ADMIN_USERNAME))
    if login_response.status == ERROR_STATUS_CODE:
        raise Exception(login_response.message)

    password_response = rpc_publisher.call(CONFIGURATION_QUEUE, GetTokenRequest(KEENETIC_ADMIN_PASSWORD))
    if password_response.status == ERROR_STATUS_CODE:
        raise Exception(password_response.message)

    config_path = os.environ[CONFIG_PATH]

    metrics_configuration = json.load(open(config_path, "r"))

    collectors = []
    keeneticClient = KeeneticClient(admin_endpoint_response.message, login_response.message, password_response.message)

    for metric_configuration in metrics_configuration['metrics']:

        _command: str = metric_configuration['command']
        # if _command != 'ntce hosts':
        #     continue
        _params = metric_configuration.get('param', {})
        _root = parse(metric_configuration['root'])
        _tags = json_path_init(metric_configuration['tags'])
        _values = json_path_init(metric_configuration['values'])

        collectors.append(KeeneticCollector(_command, _params, _root, _tags, _values))

    aiohHttpServer = AiohttpHttpServer(6789)
    aiohHttpServer.add_get_handler([HttpRoute(HTTPMethod.GET, f'{METRICS_API}', GetMetricsRequestExecutor(keeneticClient, collectors))])

    aiohHttpServer.serve_forever()

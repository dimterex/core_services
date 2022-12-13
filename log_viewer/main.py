import os
import time
import warnings

from modules.core.http_server.core_http_server import CoreHttpServer
from modules.core.http_server.web_socket import WebSocketService
from log_viewer.database.log_storage import Log_Storage
from log_viewer.log_service import Log_Service
from log_viewer.messages.LogModel import LogModel
from modules.core.log_service.log_service import Logger_Service
from modules.core.rabbitmq.api_controller import Api_Controller
from modules.core.rabbitmq.messages.identificators import LOGGER_QUEUE, LOGGER_MESSAGE_TYPE, LOGGER_MESSAGE_LEVEL, \
    LOGGER_MESSAGE_APPLICATION, LOGGER_MESSAGE_TAG, LOGGER_MESSAGE_DATETIME, LOGGER_MESSAGE_MESSAGE
from modules.core.rabbitmq.receive import Consumer
from modules.core.http_server.resource_executor import ResourceExecutor
from modules.core.http_server.template_page_executor import TemplatePageExecutor

RABBIT_HOST_ENVIRON = 'RABBIT_HOST'
RABBIT_PORT_ENVIRON = 'RABBIT_PORT'
TEMPLATES_FOLDER_ENVIRON = 'TEMPLATES'
STORAGE_FOLDER_ENVIRON = 'STORAGE'


def main():
    host = os.environ[RABBIT_HOST_ENVIRON]
    templates = os.environ[TEMPLATES_FOLDER_ENVIRON]
    storage = os.environ[STORAGE_FOLDER_ENVIRON]
    raw_port = os.environ[RABBIT_PORT_ENVIRON]
    port = int(raw_port)

    logger_service = Logger_Service('LogViewer_Application')
    api_controller = Api_Controller(logger_service)
    ampq_url = f'amqp://guest:guest@{host}:{port}'

    consumer = Consumer(ampq_url, LOGGER_QUEUE, api_controller, logger_service)
    log_storage = Log_Storage(storage)
    log_service = Log_Service(log_storage)

    def write_log_action(obj):
        applicationName = obj[LOGGER_MESSAGE_APPLICATION]
        tag = obj[LOGGER_MESSAGE_TAG]
        level = obj[LOGGER_MESSAGE_LEVEL]
        datetime = obj[LOGGER_MESSAGE_DATETIME]
        message = obj[LOGGER_MESSAGE_MESSAGE]
        logModel = LogModel(applicationName, tag, level, datetime, message)
        log_service.add_log(logModel)
        ws.send_message(0, logModel.to_json())

    api_controller.configure(LOGGER_QUEUE, LOGGER_MESSAGE_TYPE, write_log_action)

    consumer.start()

    hostname = '0.0.0.0'
    websocket_port = 6788
    ws = WebSocketService(hostname, websocket_port)
    httpServer = CoreHttpServer(6789, logger_service)
    for dp, dn, filenames in os.walk(templates):
        for f in filenames:
            full_path = os.path.join(dp, f)
            html_path = full_path.replace(templates, str())
            html_path = html_path.replace('\\', '/')
            httpServer.add_handler(html_path, ResourceExecutor(full_path))
    applications = log_service.get_applications()
    httpServer.add_handler("/", TemplatePageExecutor(templates, "index.html", {'results':  applications}))

    for app in applications:
        logs = log_service.get_logs_by_application(app)
        template = {
            'results':  logs,
            'websocket_port':  websocket_port,
        }
        httpServer.add_handler(f'/{app}', TemplatePageExecutor(templates, "application_page.html", template))

    httpServer.serve_forever()


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    print('Starting')
    main()
    print('Started')
    try:
        while True:
            time.sleep(1)
    finally:
        pass
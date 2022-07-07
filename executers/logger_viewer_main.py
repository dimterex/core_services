import asyncio
import os
import socket

from modules.logger_viewer.database.log_storage import Log_Storage
from modules.logger_viewer.http_server import HttpService
from modules.logger_viewer.log_service import Log_Service
from modules.logger_viewer.messages.LogModel import LogModel
from modules.logger_viewer.pages.application_page_generator import Application_Page_Generator
from modules.logger_viewer.pages.default_page_generator import Default_Page_Generator
from modules.logger_viewer.websocket_server import WebSocketService
from modules.models.log_service import Logger_Service, DEBUG_LOG_LEVEL
from modules.rabbitmq.messages.api_controller import Api_Controller
from modules.rabbitmq.messages.identificators import LOGGER_QUEUE, LOGGER_MESSAGE_TYPE, LOGGER_MESSAGE_LEVEL, \
    LOGGER_MESSAGE_APPLICATION, LOGGER_MESSAGE_TAG, LOGGER_MESSAGE_DATETIME, LOGGER_MESSAGE_MESSAGE
from modules.rabbitmq.publisher import Publisher
from modules.rabbitmq.receive import Consumer

PORT_ENVIRON = 'PORT'
WEBSOCKET_PORT_ENVIRON = 'WEBSOCKET_PORT'

RABBIT_HOST_ENVIRON = 'RABBIT_HOST'
RABBIT_PORT_ENVIRON = 'RABBIT_PORT'
TEMPLATES_FOLDER_ENVIRON = 'TEMPLATES'
STORAGE_FOLDER_ENVIRON = 'STORAGE'


if __name__ == '__main__':
    raw_port = os.environ[PORT_ENVIRON]
    service_port = int(raw_port)

    host = os.environ[RABBIT_HOST_ENVIRON]
    templates = os.environ[TEMPLATES_FOLDER_ENVIRON]
    storage = os.environ[STORAGE_FOLDER_ENVIRON]
    raw_port = os.environ[RABBIT_PORT_ENVIRON]
    port = int(raw_port)

    raw_port = os.environ[WEBSOCKET_PORT_ENVIRON]
    websocket_port = int(raw_port)

    logger_service = Logger_Service('LogViewer_Application')
    api_controller = Api_Controller(logger_service)
    ampq_url = f'amqp://guest:guest@{host}:{port}'

    publisher = Publisher(ampq_url)

    # def send_log(log_message):
    #     if log_message is None:
    #         publisher.send_message(LOGGER_QUEUE, log_message.to_json())
    # logger_service.configure_action(send_log)

    consumer = Consumer(ampq_url, LOGGER_QUEUE, api_controller, logger_service)
    log_storage = Log_Storage(storage)
    log_service = Log_Service(log_storage)
    default_page_generator = Default_Page_Generator(log_service, templates)

    application_page_generator = Application_Page_Generator(log_service, templates, websocket_port)

    def write_log_action(obj):
        applicationName = obj[LOGGER_MESSAGE_APPLICATION]
        tag = obj[LOGGER_MESSAGE_TAG]
        level = obj[LOGGER_MESSAGE_LEVEL]
        datetime = obj[LOGGER_MESSAGE_DATETIME]
        message = obj[LOGGER_MESSAGE_MESSAGE]
        logModel = LogModel(applicationName, tag, level, datetime, message)
        log_service.add_log(logModel)
        ws.send_log(logModel)

    api_controller.configure(LOGGER_QUEUE, LOGGER_MESSAGE_TYPE, write_log_action)

    consumer.start()

    hostname = '0.0.0.0'

    serv = HttpService(hostname, service_port, log_service, default_page_generator, application_page_generator, logger_service)
    ws = WebSocketService(hostname, websocket_port)
    loop = asyncio.get_event_loop()
    coro = loop.run_in_executor(None, serv.serve_forever())
    loop.run_until_complete(coro)

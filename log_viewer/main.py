import os
import time
import warnings

from log_viewer.database.log_storage import Log_Storage
from log_viewer.log_service import Log_Service
from log_viewer.messages.LogModel import LogModel
from modules.core.log_service.log_service import Logger_Service
from modules.core.rabbitmq.api_controller import Api_Controller
from modules.core.rabbitmq.messages.identificators import LOGGER_MESSAGE_LEVEL, \
    LOGGER_MESSAGE_APPLICATION, LOGGER_MESSAGE_TAG, LOGGER_MESSAGE_DATETIME, LOGGER_MESSAGE_MESSAGE
from modules.core.rabbitmq.receive import Consumer
from modules.core.rabbitmq.rpc.rcp_api_controller import RpcApiController
from modules.core.rabbitmq.rpc.rpc_consumer import RpcConsumer

RABBIT_HOST_ENVIRON = 'RABBIT_HOST'
RABBIT_PORT_ENVIRON = 'RABBIT_PORT'
TEMPLATES_FOLDER_ENVIRON = 'TEMPLATES'
STORAGE_FOLDER_ENVIRON = 'STORAGE'


def main():
    host = os.environ[RABBIT_HOST_ENVIRON]
    storage = os.environ[STORAGE_FOLDER_ENVIRON]
    raw_port = os.environ[RABBIT_PORT_ENVIRON]
    port = int(raw_port)

    logger_service = Logger_Service()
    api_controller = Api_Controller(logger_service)
    ampq_url = f'amqp://guest:guest@{host}:{port}'

    # consumer = Consumer(ampq_url, LOGGER_QUEUE, api_controller, logger_service)
    # log_storage = Log_Storage(storage)
    #log_service = Log_Service(log_storage)

    def write_log_action(obj):
        applicationName = obj[LOGGER_MESSAGE_APPLICATION]
        tag = obj[LOGGER_MESSAGE_TAG]
        level = obj[LOGGER_MESSAGE_LEVEL]
        datetime = obj[LOGGER_MESSAGE_DATETIME]
        message = obj[LOGGER_MESSAGE_MESSAGE]
        logModel = LogModel(applicationName, tag, level, datetime, message)
        log_service.add_log(logModel)
        # ws.send_message(0, logModel.to_json())

    api_controller.configure(LOGGER_QUEUE, LOGGER_MESSAGE_TYPE, write_log_action)

    consumer.start()

    # hostname = '0.0.0.0'
    # websocket_port = 6788
    # ws = WebSocketService(hostname, websocket_port)

    rpc_api_controller = RpcApiController(logger_service)
    rcp = RpcConsumer(ampq_url, RPC_LOGGER_QUEUE, rpc_api_controller)
    rcp.start()


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
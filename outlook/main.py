import os
import time
import warnings

from modules.core.rabbitmq.messages.identificators import LOGGER_QUEUE, OUTLOOK_QUEUE
from modules.core.rabbitmq.publisher import Publisher
from modules.core.rabbitmq.rpc.rcp_api_controller import RpcApiController
from modules.core.rabbitmq.rpc.rpc_consumer import RpcConsumer
from modules.models.configuration import Configuration

from modules.core.log_service.log_service import Logger_Service
from outlook.handlers.get_events_by_date_handler import GetEventsByDateHandler
from outlook.outlook_connection import Outlook_Connection

SETTINGS_FILE = 'settings.json'
HOST_ENVIRON = 'RABBIT_HOST'
PORT_ENVIRON = 'RABBIT_PORT'


def main():
    host = os.environ[HOST_ENVIRON]
    raw_port = os.environ[PORT_ENVIRON]
    port = int(raw_port)

    logger_service = Logger_Service('Outlook_application')
    ampq_url = f'amqp://guest:guest@{host}:{port}'
    publisher = Publisher(ampq_url)

    def send_log(log_message):
        publisher.send_message(LOGGER_QUEUE, log_message.to_json())

    logger_service.configure_action(send_log)

    with open(SETTINGS_FILE, 'r', encoding='utf8') as json_file:
        raw_data = json_file.read()
        configuration = Configuration(raw_data)

    domain_login = f'{configuration.domain}\\{configuration.login}'
    outlook_connection = Outlook_Connection(configuration.outlook, configuration.email, domain_login,
                                            configuration.password, logger_service)
    api_controller = RpcApiController(logger_service)
    api_controller.subscribe(GetEventsByDateHandler(configuration, outlook_connection, logger_service))
    rcp = RpcConsumer(ampq_url, OUTLOOK_QUEUE, api_controller)
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

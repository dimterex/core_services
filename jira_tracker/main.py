import os
import time
import warnings

from jira_tracker.handlers.create_subtask_request_handler import CreateSubtaskRequestHandler
from jira_tracker.handlers.get_worklogs_request_handler import GetWorklogsRequestHandler
from jira_tracker.handlers.write_worklog_request_handler import WriteWorklogRequestHandler
from jira_tracker.jira_connection import Jira_Connection
from modules.core.rabbitmq.messages.identificators import LOGGER_QUEUE, JIRA_QUEUE
from modules.core.rabbitmq.publisher import Publisher
from modules.core.rabbitmq.rpc.rcp_api_controller import RpcApiController
from modules.core.rabbitmq.rpc.rpc_consumer import RpcConsumer
from modules.models.configuration import Configuration
from modules.core.log_service.log_service import Logger_Service

SETTINGS_FILE = 'settings.json'
HOST_ENVIRON = 'RABBIT_HOST'
PORT_ENVIRON = 'RABBIT_PORT'


def main():
    host = os.environ[HOST_ENVIRON]
    raw_port = os.environ[PORT_ENVIRON]
    port = int(raw_port)

    logger_service = Logger_Service('Jira_application')
    ampq_url = f'amqp://guest:guest@{host}:{port}'
    publisher = Publisher(ampq_url)

    def send_log(log_message):
        publisher.send_message(LOGGER_QUEUE, log_message.to_json())

    logger_service.configure_action(send_log)

    with open(SETTINGS_FILE, 'r', encoding='utf8') as json_file:
        raw_data = json_file.read()
        configuration = Configuration(raw_data)

    jira_connection = Jira_Connection(configuration.jira, configuration.login, configuration.password, logger_service)

    api_controller = RpcApiController(logger_service)
    api_controller.subscribe(WriteWorklogRequestHandler(jira_connection, logger_service))
    api_controller.subscribe(GetWorklogsRequestHandler(jira_connection, logger_service))
    api_controller.subscribe(CreateSubtaskRequestHandler(jira_connection, logger_service))
    rcp = RpcConsumer(ampq_url, JIRA_QUEUE, api_controller)
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

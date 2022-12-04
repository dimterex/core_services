import os
import time
import warnings

from todoist_api_python.api import TodoistAPI

from modules.core.rabbitmq.messages.identificators import TODOIST_QUEUE, LOGGER_QUEUE
from modules.core.rabbitmq.publisher import Publisher
from modules.core.rabbitmq.rpc.rcp_api_controller import RpcApiController
from modules.core.rabbitmq.rpc.rpc_consumer import RpcConsumer

from modules.core.log_service.log_service import Logger_Service
from todoist.handlers.get_completed_tasks_request_handler import GetCompletedTasksRequestHandler
from todoist.handlers.update_label_request_handler import UpdateLabelRequestHandler

SETTINGS_FILE = 'settings.json'
HOST_ENVIRON = 'RABBIT_HOST'
PORT_ENVIRON = 'RABBIT_PORT'

TODOIST_API_TOKEN = 'TODOIST_API_TOKEN'


def main():
    host = os.environ[HOST_ENVIRON]
    raw_port = os.environ[PORT_ENVIRON]
    todoistToken = os.environ[TODOIST_API_TOKEN]
    port = int(raw_port)
    ampq_url = f'amqp://guest:guest@{host}:{port}'

    logger_service = Logger_Service('Todoist_application')
    publisher = Publisher(ampq_url)
    def send_log(log_message):
        publisher.send_message(LOGGER_QUEUE, log_message.to_json())

    logger_service.configure_action(send_log)

    todoistApi = TodoistAPI(todoistToken)

    api_controller = RpcApiController(logger_service)
    api_controller.subscribe(GetCompletedTasksRequestHandler(todoistApi, logger_service))
    api_controller.subscribe(UpdateLabelRequestHandler(todoistApi, logger_service))
    rcp = RpcConsumer(ampq_url, TODOIST_QUEUE, api_controller)
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

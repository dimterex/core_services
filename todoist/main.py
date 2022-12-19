import os
import time
import warnings

from todoist_api_python.api import TodoistAPI

from modules.core.rabbitmq.messages.identificators import TODOIST_QUEUE
from modules.core.rabbitmq.rpc.rcp_api_controller import RpcApiController
from modules.core.rabbitmq.rpc.rpc_consumer import RpcConsumer

from modules.core.log_service.log_service import Logger_Service
from todoist.handlers.get_completed_tasks_request_handler import GetCompletedTasksRequestHandler
from todoist.handlers.update_label_request_handler import UpdateLabelRequestHandler

SETTINGS_FILE = 'settings.json'
TODOIST_API_TOKEN = 'TODOIST_API_TOKEN'
RABBIT_CONNECTION_STRING = 'RABBIT_AMPQ_URL'


def main():
    logger_service = Logger_Service()
    ampq_url = os.environ[RABBIT_CONNECTION_STRING]

    todoistToken = os.environ[TODOIST_API_TOKEN]
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

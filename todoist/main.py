import os
import time
import warnings

from todoist_api_python.api import TodoistAPI

from modules.core.rabbitmq.messages.configuration.tokens.get_token_request import GetTokenRequest
from modules.core.rabbitmq.messages.identificators import CONFIGURATION_QUEUE, TODOIST_QUEUE, TODOIST_TOKEN
from modules.core.rabbitmq.messages.status_response import ERROR_STATUS_CODE
from modules.core.rabbitmq.rpc.rcp_api_controller import RpcApiController
from modules.core.rabbitmq.rpc.rpc_consumer import RpcConsumer

from modules.core.log_service.log_service import Logger_Service
from modules.core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from todoist.handlers.add_task_request_handler import AddTaskRequestHandler
from todoist.handlers.get_completed_tasks_request_handler import GetCompletedTasksRequestHandler
from todoist.handlers.update_label_request_handler import UpdateLabelRequestHandler

RABBIT_CONNECTION_STRING = 'RABBIT_AMPQ_URL'


def main():
    logger_service = Logger_Service()
    ampq_url = os.environ[RABBIT_CONNECTION_STRING]
    rpc_publisher = RpcPublisher(ampq_url)

    token_response = rpc_publisher.call(CONFIGURATION_QUEUE, GetTokenRequest(TODOIST_TOKEN))

    if token_response.status == ERROR_STATUS_CODE:
        raise Exception(token_response.message)

    todoistApi = TodoistAPI(str(token_response.message))

    api_controller = RpcApiController(logger_service)
    api_controller.subscribe(GetCompletedTasksRequestHandler(todoistApi, logger_service))
    api_controller.subscribe(UpdateLabelRequestHandler(todoistApi, logger_service))
    api_controller.subscribe(AddTaskRequestHandler(todoistApi, logger_service))
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

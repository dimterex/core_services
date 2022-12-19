import os
import time
import warnings

from jira_tracker.handlers.create_subtask_request_handler import CreateSubtaskRequestHandler
from jira_tracker.handlers.get_worklogs_request_handler import GetWorklogsRequestHandler
from jira_tracker.handlers.write_worklog_request_handler import WriteWorklogRequestHandler
from jira_tracker.jira_connection import Jira_Connection
from modules.core.rabbitmq.messages.configuration.credentials.credential_model import CredentialModel
from modules.core.rabbitmq.messages.configuration.credentials.get_credentials_request import GetCredentialsRequest
from modules.core.rabbitmq.messages.configuration.urls.get_url_request import GetUrlRequest
from modules.core.rabbitmq.messages.identificators import CONFIGURATION_QUEUE, JIRA_QUEUE, JIRA_URL_TYPE
from modules.core.rabbitmq.messages.status_response import ERROR_STATUS_CODE
from modules.core.rabbitmq.rpc.rcp_api_controller import RpcApiController
from modules.core.rabbitmq.rpc.rpc_consumer import RpcConsumer
from modules.core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from modules.core.log_service.log_service import Logger_Service

RABBIT_CONNECTION_STRING = 'RABBIT_AMPQ_URL'


def main():
    ampq_url = os.environ[RABBIT_CONNECTION_STRING]
    logger_service = Logger_Service()

    rpc_publisher = RpcPublisher(ampq_url)
    credentials_response = rpc_publisher.call(CONFIGURATION_QUEUE, GetCredentialsRequest())

    if credentials_response.status == ERROR_STATUS_CODE:
        raise Exception(credentials_response.message)

    credentials = CredentialModel.deserialize(credentials_response.message)
    get_url_response = rpc_publisher.call(CONFIGURATION_QUEUE, GetUrlRequest(JIRA_URL_TYPE))

    if get_url_response.status == ERROR_STATUS_CODE:
        raise Exception(get_url_response.message)

    jira_connection = Jira_Connection(credentials, str(get_url_response.message))

    api_controller = RpcApiController(logger_service)
    api_controller.subscribe(WriteWorklogRequestHandler(jira_connection, logger_service))
    api_controller.subscribe(GetWorklogsRequestHandler(credentials, jira_connection, logger_service))
    api_controller.subscribe(CreateSubtaskRequestHandler(credentials, jira_connection, logger_service))
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

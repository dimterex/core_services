import os
import time
import warnings

from modules.core.rabbitmq.messages.configuration.credentials.credential_model import CredentialModel
from modules.core.rabbitmq.messages.configuration.credentials.get_credentials_request import GetCredentialsRequest
from modules.core.rabbitmq.messages.configuration.urls.get_url_request import GetUrlRequest
from modules.core.rabbitmq.messages.identificators import CONFIGURATION_QUEUE, OUTLOOK_URL_TYPE, \
    OUTLOOK_QUEUE
from modules.core.rabbitmq.messages.status_response import ERROR_STATUS_CODE
from modules.core.rabbitmq.rpc.rcp_api_controller import RpcApiController
from modules.core.rabbitmq.rpc.rpc_consumer import RpcConsumer
from modules.core.rabbitmq.rpc.rpc_publisher import RpcPublisher

from modules.core.log_service.log_service import Logger_Service
from outlook.handlers.get_events_by_date_handler import GetEventsByDateHandler
from outlook.outlook_connection import Outlook_Connection

RABBIT_CONNECTION_STRING = 'RABBIT_AMPQ_URL'


def main():
    logger_service = Logger_Service()
    ampq_url = os.environ[RABBIT_CONNECTION_STRING]

    rpc_publisher = RpcPublisher(ampq_url)
    credentials_response = rpc_publisher.call(CONFIGURATION_QUEUE, GetCredentialsRequest())

    if credentials_response.status == ERROR_STATUS_CODE:
        raise Exception(credentials_response.message)

    credentials = CredentialModel.deserialize(credentials_response.message)
    get_url_response = rpc_publisher.call(CONFIGURATION_QUEUE, GetUrlRequest(OUTLOOK_URL_TYPE))

    if get_url_response.status == ERROR_STATUS_CODE:
        raise Exception(get_url_response.message)

    domain_login = f'{credentials.domain}\\{credentials.login}'
    outlook_connection = Outlook_Connection(str(get_url_response.message), domain_login, credentials, logger_service)
    api_controller = RpcApiController(logger_service)
    api_controller.subscribe(GetEventsByDateHandler(outlook_connection, logger_service))
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

import os
import re
import time
import warnings

from core.log_service.log_service import Logger_Service
from core.rabbitmq.messages.configuration.tokens.get_token_request import GetTokenRequest
from core.rabbitmq.messages.identificators import CONFIGURATION_QUEUE, TELEGRAM_TOKEN
from core.rabbitmq.messages.status_response import ERROR_STATUS_CODE
from core.rabbitmq.rpc.rcp_api_controller import RpcApiController
from core.rabbitmq.rpc.rpc_publisher import RpcPublisher

from models.telegram_bot import TelegramBot
from telegram_bot.models.commands.file_download_command import FileDownloadCommand
from telegram_bot.models.commands.pip_download_command import PipDownloadCommand
from telegram_bot.models.commands.webpage_download_command import WebpageDownloadCommand

RABBIT_CONNECTION_STRING = 'RABBIT_AMPQ_URL'
DOWNLOAD_DIRECTORY_PATH = 'DOWNLOAD_DIRECTORY_PATH'


def main():
    logger_service = Logger_Service()
    ampq_url = os.environ[RABBIT_CONNECTION_STRING]
    temp_folder_path = os.environ[DOWNLOAD_DIRECTORY_PATH]
    rpc_publisher = RpcPublisher(ampq_url)

    token_response = rpc_publisher.call(CONFIGURATION_QUEUE, GetTokenRequest(TELEGRAM_TOKEN))

    if token_response.status == ERROR_STATUS_CODE:
        raise Exception(token_response.message)

    # api_controller = RpcApiController(logger_service)
    # api_controller.subscribe(GetCompletedTasksRequestHandler(todoistApi, logger_service))

    # api_controller.subscribe(AddTaskRequestHandler(todoistApi, logger_service))
    # rcp = RpcConsumer(ampq_url, TODOIST_QUEUE, api_controller)
    # rcp.start()
    # path = ''
    telegram_bot = TelegramBot(token_response.message,
                               PipDownloadCommand(temp_folder_path),
                               WebpageDownloadCommand(temp_folder_path, logger_service),
                               FileDownloadCommand(temp_folder_path))
    telegram_bot.start()


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

import datetime
import os
import time
import warnings

from modules.core.log_service.log_service import Logger_Service
from modules.core.rabbitmq.rpc.rcp_api_controller import RpcApiController
from modules.core.rabbitmq.rpc.rpc_consumer import RpcConsumer
from modules.core.rabbitmq.messages.identificators import LOGGER_QUEUE, WORKLOG_QUEUE
from modules.core.rabbitmq.publisher import Publisher
from modules.models.configuration import Configuration
from worklog_kpi.handlers.get_history_by_date_worklog_request_handler import GetHistoryByDateWorklogRequestHandler
from worklog_kpi.handlers.write_worklog_request_handler import Write_Worklog_Request_Handler
from worklog_kpi.models.worklog_sqlite_model import WorklogSqliteModel
from worklog_kpi.services.worklog_storage_service import WorklogStorageService
from worklog_kpi.write_worklog_action import Write_WorkLok_Action

SETTINGS_FILE = 'settings.json'
HOST_ENVIRON = 'RABBIT_HOST'
PORT_ENVIRON = 'RABBIT_PORT'
STORAGE_FOLDER_ENVIRON = 'STORAGE'



def main():

    host = os.environ[HOST_ENVIRON]
    raw_port = os.environ[PORT_ENVIRON]
    storage = os.environ[STORAGE_FOLDER_ENVIRON]
    port = int(raw_port)

    logger_service = Logger_Service('Worklog_Application')
    api_controller = RpcApiController(logger_service)

    ampq_url = f'amqp://guest:guest@{host}:{port}'
    publisher = Publisher(ampq_url)

    storage = WorklogStorageService(storage, logger_service)
    def send_log(log_message):
        publisher.send_message(LOGGER_QUEUE, log_message.to_json())

    logger_service.configure_action(send_log)

    with open(SETTINGS_FILE, 'r', encoding='utf8') as json_file:
        raw_data = json_file.read()
        configuration = Configuration(raw_data)

    write_WorkLok_Action = Write_WorkLok_Action(configuration, publisher, logger_service, storage)
    api_controller.subscribe(Write_Worklog_Request_Handler(write_WorkLok_Action))
    api_controller.subscribe(GetHistoryByDateWorklogRequestHandler(storage))

    rcp = RpcConsumer(ampq_url, WORKLOG_QUEUE, api_controller)
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


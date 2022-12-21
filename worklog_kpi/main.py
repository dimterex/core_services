import os
import time
import warnings

from modules.core.log_service.log_service import Logger_Service
from modules.core.rabbitmq.rpc.rcp_api_controller import RpcApiController
from modules.core.rabbitmq.rpc.rpc_consumer import RpcConsumer
from modules.core.rabbitmq.messages.identificators import WORKLOG_QUEUE
from modules.core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from worklog_kpi.handlers.get_history_by_date_worklog_request_handler import GetHistoryByDateWorklogRequestHandler
from worklog_kpi.handlers.write_worklog_request_handler import Write_Worklog_Request_Handler
from worklog_kpi.services.worklog_storage_service import WorklogStorageService
from worklog_kpi.write_worklog_action import Write_WorkLok_Action

STORAGE_FOLDER_ENVIRON = 'STORAGE'
RABBIT_CONNECTION_STRING = 'RABBIT_AMPQ_URL'


def main():
    logger_service = Logger_Service()
    ampq_url = os.environ[RABBIT_CONNECTION_STRING]
    storage = os.environ[STORAGE_FOLDER_ENVIRON]

    api_controller = RpcApiController(logger_service)
    publisher = RpcPublisher(ampq_url)

    storage = WorklogStorageService(storage, logger_service)

    write_WorkLok_Action = Write_WorkLok_Action(publisher, logger_service, storage)

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


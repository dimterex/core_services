from datetime import datetime

from core.rabbitmq.messages.configuration.periodical_task_model import PeriodicalTaskModel
from core.rabbitmq.messages.configuration.periodical_tasks.get_periodical_tasks_request import \
    GetPeriodicalTasksRequest
from core.rabbitmq.messages.identificators import CONFIGURATION_QUEUE
from core.rabbitmq.messages.status_response import SUCCESS_STATUS_CODE
from core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from core.log_service.log_service import Logger_Service
from worklog_kpi.services.worklog_service import Worklog_Service


class Worklog_By_Periodical:
    def __init__(self,
                 start_time: datetime,
                 rpcPublisher: RpcPublisher,
                 worklog_service: Worklog_Service,
                 logger_service: Logger_Service):
        self.rpcPublisher = rpcPublisher
        self.logger_service = logger_service
        self.worklog_service = worklog_service
        self.start_time = start_time

    def modify(self):
        self.logger_service.debug(self.__class__.__name__, 'Starting modify')
        response = self.rpcPublisher.call(CONFIGURATION_QUEUE, GetPeriodicalTasksRequest())

        if response.status == SUCCESS_STATUS_CODE:
            for rawTask in response.message:
                task = PeriodicalTaskModel.deserialize(rawTask)
                self.worklog_service.add_worklog(task.name, self.start_time.replace(hour=7), task.tracker_id, task.duration)
            self.worklog_service.from_config = True
            self.logger_service.debug(self.__class__.__name__, 'Ending modify')
        else:
            raise Exception(response.message)

from configuration.database.periodical_tasks_table import PeriodicalTasksTable
from modules.core.rabbitmq.messages.configuration.periodical_tasks.add_new_periodical_task_request import \
    ADD_NEW_PERIODICAL_TASK_REQUEST_MESSAGE_TYPE
from modules.core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class AddNewPeriodicalTaskRequestHandler(RpcBaseHandler):
    def __init__(self, storage: PeriodicalTasksTable):
        super().__init__(ADD_NEW_PERIODICAL_TASK_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            new_id = self.storage.add_new_task()
            return StatusResponse(new_id)
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)

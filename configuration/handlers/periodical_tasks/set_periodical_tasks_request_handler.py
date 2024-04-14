from configuration.database.periodical_tasks_table import PeriodicalTasksTable
from core.rabbitmq.messages.configuration.periodical_tasks.set_periodical_tasks_request import \
    SET_PERIODICAL_TASKS_REQUEST_MESSAGE_TYPE, SetPeriodicalTasksRequest
from core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse
from core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class SetPeriodicalTasksRequestHandler(RpcBaseHandler):
    def __init__(self, storage: PeriodicalTasksTable):
        super().__init__(SET_PERIODICAL_TASKS_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            request = SetPeriodicalTasksRequest.deserialize(payload)
            self.storage.set_periodical_tasks(request.tasks)
            return StatusResponse('Done')
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)

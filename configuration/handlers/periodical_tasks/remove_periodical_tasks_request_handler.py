from configuration.database.periodical_tasks_table import PeriodicalTasksTable
from modules.core.rabbitmq.messages.configuration.periodical_tasks.remove_periodical_tasks_request import \
    REMOVE_PERIODICAL_TASKS_REQUEST_MESSAGE_TYPE, RemovePeriodicalTasksRequest
from modules.core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class RemovePeriodicalTasksRequestHandler(RpcBaseHandler):
    def __init__(self, storage: PeriodicalTasksTable):
        super().__init__(REMOVE_PERIODICAL_TASKS_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            request = RemovePeriodicalTasksRequest.deserialize(payload)
            self.storage.remove(request.ids)
            return StatusResponse("Done")
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)

from configuration.database.periodical_tasks_table import PeriodicalTasksTable
from core.rabbitmq.messages.configuration.periodical_tasks.get_periodical_tasks_request import \
    GET_PERIODICAL_TASKS_REQUEST_MESSAGE_TYPE
from core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class GetPeriodicalTasksRequestHandler(RpcBaseHandler):
    def __init__(self, storage: PeriodicalTasksTable):
        super().__init__(GET_PERIODICAL_TASKS_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            tokens = self.storage.get_periodical_tasks()
            js = []
            for token in tokens:
                js.append(token.serialize())
            return StatusResponse(js)
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)

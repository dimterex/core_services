from jira_tracker.models.history_service import History_Service
from modules.core.rabbitmq.messages.jira_tracker.get_worklogs_request import GET_WORKLOGS_REQUEST_MESSAGE_TYPE, GetWorklogsRequest
from modules.core.log_service.log_service import Logger_Service
from modules.core.rabbitmq.messages.status_response import StatusResponse
from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class GetWorklogsRequestHandler(RpcBaseHandler):
    def __init__(self, historyService: History_Service, logger_service: Logger_Service):
        super().__init__(GET_WORKLOGS_REQUEST_MESSAGE_TYPE)
        self.historyService = historyService
        self.logger_service = logger_service
        self.TAG = self.__class__.__name__

    def execute(self, payload) -> StatusResponse:
        request = GetWorklogsRequest.deserialize(payload)
        statistics = self.historyService.get_statistic(request.year, request.month)
        result = []

        for statistic in statistics:
            result.append(statistic.to_json())

        return StatusResponse(result)

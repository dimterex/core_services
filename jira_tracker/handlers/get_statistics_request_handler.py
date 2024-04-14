from jira_tracker.models.history_service import History_Service
from core.rabbitmq.messages.jira_tracker.get_statistics_request import GET_STATISTICS_REQUEST_MESSAGE_TYPE, GetStatisticsRequest
from core.log_service.log_service import Logger_Service
from core.rabbitmq.messages.status_response import StatusResponse
from core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class GetStatisticsRequestHandler(RpcBaseHandler):
    def __init__(self, historyService: History_Service, logger_service: Logger_Service):
        super().__init__(GET_STATISTICS_REQUEST_MESSAGE_TYPE)
        self.historyService = historyService
        self.logger_service = logger_service
        self.TAG = self.__class__.__name__

    def execute(self, payload) -> StatusResponse:
        request = GetStatisticsRequest.deserialize(payload)
        statistics = self.historyService.get_statistic(request.year, request.month)
        result = []

        for statistic in statistics:
            result.append(statistic.serialize())

        return StatusResponse(result)

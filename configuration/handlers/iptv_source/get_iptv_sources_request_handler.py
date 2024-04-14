from configuration.database.iptv_sources_table import IptvSourcesTable
from core.rabbitmq.messages.configuration.iptv_sources.get_iptv_sources_request import \
    GET_IPTV_SOURCES_REQUEST_MESSAGE_TYPE
from core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from core.log_service.log_service import Logger_Service
from core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class GetIptvSourcesRequestHandler(RpcBaseHandler, Logger_Service):
    def __init__(self, storage: IptvSourcesTable):
        super().__init__(GET_IPTV_SOURCES_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            data = self.storage.get_sources()
            response = []
            for source in data:
                response.append(source.serialize())
            return StatusResponse(response)
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
